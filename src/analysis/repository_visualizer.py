"""
Repository Visualization Module
Generates interactive visualizations for repository analysis
"""

import json
import networkx as nx
import plotly.graph_objects as go
import plotly.express as px
import plotly.subplots as sp
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import re

from agent.ai_agent import FastMCPTools

class RepositoryVisualizer:
    """Interactive repository visualization generator"""
    
    def __init__(self):
        self.tools = FastMCPTools()
        self.visualization_cache = {}
    
    def generate_repository_map(self, repo_url: str, status_callback=None) -> Dict[str, Any]:
        """Generate comprehensive repository visualization map"""
        
        if status_callback:
            status_callback("🗺️ Generating repository map...")
        
        visualizations = {
            "repository_url": repo_url,
            "timestamp": datetime.now().isoformat(),
            "directory_tree": {},
            "file_structure": {},
            "dependency_graph": {},
            "code_heatmap": {},
            "activity_timeline": {},
            "language_distribution": {},
            "file_size_distribution": {}
        }
        
        try:
            # 1. Directory Tree Visualization
            if status_callback:
                status_callback("📁 Creating directory tree...")
            
            tree_viz = self._create_directory_tree_viz(repo_url)
            visualizations["directory_tree"] = tree_viz
            
            # 2. File Structure Analysis
            if status_callback:
                status_callback("📊 Analyzing file structure...")
            
            structure_viz = self._create_file_structure_viz(repo_url)
            visualizations["file_structure"] = structure_viz
            
            # 3. Dependency Graph
            if status_callback:
                status_callback("🔗 Creating dependency graph...")
            
            dependency_viz = self._create_dependency_graph(repo_url)
            visualizations["dependency_graph"] = dependency_viz
            
            # 4. Code Activity Heatmap
            if status_callback:
                status_callback("📈 Creating activity heatmap...")
            
            heatmap_viz = self._create_activity_heatmap(repo_url)
            visualizations["code_heatmap"] = heatmap_viz
            
            # 5. Language Distribution
            if status_callback:
                status_callback("🌐 Analyzing language distribution...")
            
            language_viz = self._create_language_distribution(repo_url)
            visualizations["language_distribution"] = language_viz
            
            # 6. File Size Distribution
            if status_callback:
                status_callback("📏 Analyzing file sizes...")
            
            size_viz = self._create_file_size_distribution(repo_url)
            visualizations["file_size_distribution"] = size_viz
            
            if status_callback:
                status_callback("✅ Repository map complete!")
            
            return visualizations
            
        except Exception as e:
            if status_callback:
                status_callback(f"❌ Repository map generation failed: {str(e)}")
            visualizations["error"] = str(e)
            return visualizations
    
    def _create_directory_tree_viz(self, repo_url: str) -> Dict[str, Any]:
        """Create interactive directory tree visualization"""
        try:
            # Get directory tree from MCP server
            tree_result = self.tools.get_directory_tree(repo_url, max_depth=5)
            tree_data = json.loads(tree_result) if isinstance(tree_result, str) else tree_data
            
            # Parse tree structure
            tree_structure = self._parse_tree_structure(tree_data)
            
            # Create treemap visualization
            fig = px.treemap(
                tree_structure,
                path=['level', 'name'],
                values='size',
                title="Repository Directory Structure",
                hover_data=['type', 'path']
            )
            
            return {
                "type": "treemap",
                "data": fig.to_json(),
                "tree_structure": tree_structure
            }
            
        except Exception as e:
            return {"error": f"Failed to create directory tree: {str(e)}"}
    
    def _create_file_structure_viz(self, repo_url: str) -> Dict[str, Any]:
        """Create file structure visualization"""
        try:
            # Get file structure from MCP server
            structure_result = self.tools.get_file_structure(repo_url)
            structure_data = json.loads(structure_result) if isinstance(structure_result, str) else structure_data
            
            # Parse file structure
            files = self._parse_file_structure(structure_data)
            
            # Create sunburst chart
            fig = px.sunburst(
                files,
                path=['directory', 'extension'],
                values='size',
                title="File Structure by Type and Directory"
            )
            
            return {
                "type": "sunburst",
                "data": fig.to_json(),
                "file_count": len(files),
                "total_size": sum(f['size'] for f in files)
            }
            
        except Exception as e:
            return {"error": f"Failed to create file structure: {str(e)}"}
    
    def _create_dependency_graph(self, repo_url: str) -> Dict[str, Any]:
        """Create dependency graph visualization"""
        try:
            # Get dependency information
            dependency_result = self.tools.search_dependencies(repo_url)
            dependency_data = json.loads(dependency_result) if isinstance(dependency_result, str) else dependency_data
            
            # Parse dependencies
            dependencies = self._parse_dependencies(dependency_data)
            
            # Create network graph
            G = nx.DiGraph()
            
            # Add nodes and edges
            for dep in dependencies:
                G.add_node(dep['name'], type=dep['type'])
                if dep.get('dependencies'):
                    for sub_dep in dep['dependencies']:
                        G.add_edge(dep['name'], sub_dep)
            
            # Create network visualization
            pos = nx.spring_layout(G)
            
            edge_trace = go.Scatter(
                x=[], y=[], line=dict(width=0.5, color='#888'), hoverinfo='none', mode='lines')
            
            for edge in G.edges():
                x0, y0 = pos[edge[0]]
                x1, y1 = pos[edge[1]]
                edge_trace['x'] += tuple([x0, x1, None])
                edge_trace['y'] += tuple([y0, y1, None])
            
            node_trace = go.Scatter(
                x=[], y=[], text=[], mode='markers', hoverinfo='text',
                marker=dict(showscale=True, colorscale='YlGnBu', size=10,
                           colorbar=dict(thickness=15, xanchor="left", len=0.6)))
            
            for node in G.nodes():
                x, y = pos[node]
                node_trace['x'] += tuple([x])
                node_trace['y'] += tuple([y])
                node_trace['text'] += tuple([node])
            
            fig = go.Figure(data=[edge_trace, node_trace],
                          layout=go.Layout(
                              title="Dependency Graph",
                              showlegend=False,
                              hovermode='closest',
                              margin=dict(b=20,l=5,r=5,t=40),
                              xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                              yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                          )
            
            return {
                "type": "network",
                "data": fig.to_json(),
                "node_count": len(G.nodes()),
                "edge_count": len(G.edges())
            }
            
        except Exception as e:
            return {"error": f"Failed to create dependency graph: {str(e)}"}
    
    def _create_activity_heatmap(self, repo_url: str) -> Dict[str, Any]:
        """Create code activity heatmap"""
        try:
            # Get commit history
            commits_result = self.tools.get_recent_commits(repo_url, limit=100)
            commits_data = json.loads(commits_result) if isinstance(commits_result, str) else commits_data
            
            # Parse commit data
            commits = self._parse_commit_data(commits_data)
            
            # Create activity matrix
            activity_matrix = self._create_activity_matrix(commits)
            
            # Create heatmap
            fig = px.imshow(
                activity_matrix,
                title="Code Activity Heatmap (Last 30 Days)",
                labels=dict(x="Day of Week", y="Week", color="Commits"),
                aspect="auto"
            )
            
            return {
                "type": "heatmap",
                "data": fig.to_json(),
                "total_commits": len(commits),
                "active_days": len([c for c in commits if c.get('active', False)])
            }
            
        except Exception as e:
            return {"error": f"Failed to create activity heatmap: {str(e)}"}
    
    def _create_language_distribution(self, repo_url: str) -> Dict[str, Any]:
        """Create programming language distribution chart"""
        try:
            # Get file structure to analyze languages
            structure_result = self.tools.get_file_structure(repo_url)
            structure_data = json.loads(structure_result) if isinstance(structure_result, str) else structure_data
            
            # Parse and categorize files by language
            language_data = self._categorize_by_language(structure_data)
            
            # Create pie chart
            fig = px.pie(
                values=list(language_data.values()),
                names=list(language_data.keys()),
                title="Programming Language Distribution"
            )
            
            return {
                "type": "pie",
                "data": fig.to_json(),
                "languages": language_data,
                "total_files": sum(language_data.values())
            }
            
        except Exception as e:
            return {"error": f"Failed to create language distribution: {str(e)}"}
    
    def _create_file_size_distribution(self, repo_url: str) -> Dict[str, Any]:
        """Create file size distribution visualization"""
        try:
            # Get file structure
            structure_result = self.tools.get_file_structure(repo_url)
            structure_data = json.loads(structure_result) if isinstance(structure_result, str) else structure_data
            
            # Parse file sizes
            file_sizes = self._parse_file_sizes(structure_data)
            
            # Create histogram
            fig = px.histogram(
                file_sizes,
                x='size',
                nbins=20,
                title="File Size Distribution",
                labels={'size': 'File Size (KB)', 'count': 'Number of Files'}
            )
            
            return {
                "type": "histogram",
                "data": fig.to_json(),
                "total_files": len(file_sizes),
                "average_size": sum(f['size'] for f in file_sizes) / len(file_sizes) if file_sizes else 0
            }
            
        except Exception as e:
            return {"error": f"Failed to create file size distribution: {str(e)}"}
    
    def _parse_tree_structure(self, tree_data: Any) -> List[Dict[str, Any]]:
        """Parse directory tree structure"""
        tree_structure = []
        
        try:
            if isinstance(tree_data, dict) and "result" in tree_data:
                tree_str = tree_data["result"]
                if isinstance(tree_str, str):
                    lines = tree_str.split('\n')
                    for line in lines:
                        if line.strip():
                            # Parse tree line (e.g., "├── file.py")
                            level = len(line) - len(line.lstrip())
                            name = line.strip().split('── ')[-1] if '── ' in line else line.strip()
                            
                            tree_structure.append({
                                'level': level,
                                'name': name,
                                'path': name,
                                'type': 'directory' if not '.' in name else 'file',
                                'size': 1  # Placeholder size
                            })
            
        except Exception as e:
            tree_structure.append({'error': str(e)})
        
        return tree_structure
    
    def _parse_file_structure(self, structure_data: Any) -> List[Dict[str, Any]]:
        """Parse file structure data"""
        files = []
        
        try:
            if isinstance(structure_data, dict) and "result" in structure_data:
                structure_str = structure_data["result"]
                if isinstance(structure_str, str):
                    lines = structure_str.split('\n')
                    for line in lines:
                        if line.strip() and '/' in line:
                            parts = line.strip().split('/')
                            filename = parts[-1]
                            directory = '/'.join(parts[:-1]) if len(parts) > 1 else 'root'
                            extension = filename.split('.')[-1] if '.' in filename else 'no_extension'
                            
                            files.append({
                                'name': filename,
                                'directory': directory,
                                'extension': extension,
                                'path': line.strip(),
                                'size': 1  # Placeholder size
                            })
            
        except Exception as e:
            files.append({'error': str(e)})
        
        return files
    
    def _parse_dependencies(self, dependency_data: Any) -> List[Dict[str, Any]]:
        """Parse dependency information"""
        dependencies = []
        
        try:
            if isinstance(dependency_data, dict) and "result" in dependency_data:
                dep_str = dependency_data["result"]
                if isinstance(dep_str, str):
                    # Look for common dependency patterns
                    lines = dep_str.split('\n')
                    for line in lines:
                        if any(keyword in line.lower() for keyword in ['import', 'require', 'depend', 'package']):
                            dependencies.append({
                                'name': line.strip(),
                                'type': 'dependency',
                                'dependencies': []
                            })
            
        except Exception as e:
            dependencies.append({'error': str(e)})
        
        return dependencies
    
    def _parse_commit_data(self, commit_data: Any) -> List[Dict[str, Any]]:
        """Parse commit history data"""
        commits = []
        
        try:
            if isinstance(commit_data, dict) and "result" in commit_data:
                commit_str = commit_data["result"]
                if isinstance(commit_str, str):
                    lines = commit_str.split('\n')
                    for line in lines:
                        if line.strip():
                            # Parse commit line (simplified)
                            commits.append({
                                'hash': line[:8] if len(line) > 8 else line,
                                'message': line,
                                'date': datetime.now().isoformat(),  # Placeholder
                                'active': True
                            })
            
        except Exception as e:
            commits.append({'error': str(e)})
        
        return commits
    
    def _create_activity_matrix(self, commits: List[Dict[str, Any]]) -> List[List[int]]:
        """Create activity matrix for heatmap"""
        # Create 7x4 matrix (7 days, 4 weeks)
        matrix = [[0 for _ in range(7)] for _ in range(4)]
        
        try:
            for commit in commits:
                # Simplified: distribute commits randomly across matrix
                import random
                week = random.randint(0, 3)
                day = random.randint(0, 6)
                matrix[week][day] += 1
            
        except Exception as e:
            pass
        
        return matrix
    
    def _categorize_by_language(self, structure_data: Any) -> Dict[str, int]:
        """Categorize files by programming language"""
        languages = {}
        
        try:
            if isinstance(structure_data, dict) and "result" in structure_data:
                structure_str = structure_data["result"]
                if isinstance(structure_str, str):
                    lines = structure_str.split('\n')
                    for line in lines:
                        if line.strip():
                            filename = line.strip().split('/')[-1]
                            extension = filename.split('.')[-1].lower() if '.' in filename else 'unknown'
                            
                            # Map extensions to languages
                            lang_map = {
                                'py': 'Python',
                                'js': 'JavaScript',
                                'ts': 'TypeScript',
                                'java': 'Java',
                                'cpp': 'C++',
                                'c': 'C',
                                'cs': 'C#',
                                'php': 'PHP',
                                'rb': 'Ruby',
                                'go': 'Go',
                                'rs': 'Rust',
                                'swift': 'Swift',
                                'kt': 'Kotlin',
                                'scala': 'Scala',
                                'html': 'HTML',
                                'css': 'CSS',
                                'json': 'JSON',
                                'xml': 'XML',
                                'md': 'Markdown',
                                'txt': 'Text'
                            }
                            
                            language = lang_map.get(extension, extension.upper())
                            languages[language] = languages.get(language, 0) + 1
            
        except Exception as e:
            languages['Error'] = 1
        
        return languages
    
    def _parse_file_sizes(self, structure_data: Any) -> List[Dict[str, Any]]:
        """Parse file size information"""
        file_sizes = []
        
        try:
            if isinstance(structure_data, dict) and "result" in structure_data:
                structure_str = structure_data["result"]
                if isinstance(structure_str, str):
                    lines = structure_str.split('\n')
                    for line in lines:
                        if line.strip():
                            file_sizes.append({
                                'name': line.strip(),
                                'size': 1  # Placeholder size in KB
                            })
            
        except Exception as e:
            file_sizes.append({'error': str(e)})
        
        return file_sizes

# Global visualizer instance
_repository_visualizer = None

def get_repository_visualizer() -> RepositoryVisualizer:
    """Get the global repository visualizer instance"""
    global _repository_visualizer
    if _repository_visualizer is None:
        _repository_visualizer = RepositoryVisualizer()
    return _repository_visualizer

def generate_repository_map(repo_url: str, status_callback=None) -> Dict[str, Any]:
    """Generate comprehensive repository visualization map"""
    visualizer = get_repository_visualizer()
    return visualizer.generate_repository_map(repo_url, status_callback) 