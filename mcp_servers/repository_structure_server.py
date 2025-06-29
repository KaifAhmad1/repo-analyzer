"""
Repository Structure MCP Server

This server provides tools for analyzing and navigating repository structure,
including directory trees, file listings, and structural analysis.
"""

from typing import Dict, List, Optional, Any
from pathlib import Path
import re

from .base_server import BaseMCPServer

class RepositoryStructureServer(BaseMCPServer):
    """
    MCP Server for repository structure analysis.
    
    Tools provided:
    - get_repository_tree: Get complete directory tree
    - analyze_structure: Analyze repository structure patterns
    - find_files_by_type: Find files by extension or type
    - get_directory_stats: Get statistics about directories
    - identify_project_type: Identify project type based on structure
    """
    
    def __init__(self):
        super().__init__(
            name="repository_structure_server",
            description="Server for analyzing repository structure and file organization"
        )
        
    async def initialize_tools(self) -> List[Dict[str, Any]]:
        """
        Initialize tools for repository structure analysis.
        """
        tools = [
            {
                "name": "get_repository_tree",
                "description": "Get the complete directory tree structure of a repository",
                "parameters": {
                    "repository": "string (required): Repository name in format 'owner/repo'",
                    "branch": "string (optional): Branch name, defaults to 'main'",
                    "max_depth": "integer (optional): Maximum depth to traverse, defaults to 5",
                    "include_files": "boolean (optional): Include files in tree, defaults to true"
                }
            },
            {
                "name": "analyze_structure",
                "description": "Analyze repository structure patterns and organization",
                "parameters": {
                    "repository": "string (required): Repository name in format 'owner/repo'",
                    "branch": "string (optional): Branch name, defaults to 'main'"
                }
            },
            {
                "name": "find_files_by_type",
                "description": "Find files by extension or file type",
                "parameters": {
                    "repository": "string (required): Repository name in format 'owner/repo'",
                    "file_extensions": "array (optional): List of file extensions to search for",
                    "file_types": "array (optional): List of file types (e.g., 'image', 'document')",
                    "branch": "string (optional): Branch name, defaults to 'main'",
                    "recursive": "boolean (optional): Search recursively, defaults to true"
                }
            },
            {
                "name": "get_directory_stats",
                "description": "Get statistics about directories and file distribution",
                "parameters": {
                    "repository": "string (required): Repository name in format 'owner/repo'",
                    "directory_path": "string (optional): Specific directory to analyze, defaults to root",
                    "branch": "string (optional): Branch name, defaults to 'main'"
                }
            },
            {
                "name": "identify_project_type",
                "description": "Identify project type based on structure and files",
                "parameters": {
                    "repository": "string (required): Repository name in format 'owner/repo'",
                    "branch": "string (optional): Branch name, defaults to 'main'"
                }
            },
            {
                "name": "get_common_patterns",
                "description": "Find common file and directory patterns in the repository",
                "parameters": {
                    "repository": "string (required): Repository name in format 'owner/repo'",
                    "branch": "string (optional): Branch name, defaults to 'main'",
                    "pattern_type": "string (optional): Type of patterns to find ('naming', 'structure', 'all')"
                }
            }
        ]
        return tools
    
    async def handle_tool_call(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """
        Handle repository structure tool calls.
        """
        try:
            if tool_name == "get_repository_tree":
                return await self._get_repository_tree(**arguments)
            elif tool_name == "analyze_structure":
                return await self._analyze_structure(**arguments)
            elif tool_name == "find_files_by_type":
                return await self._find_files_by_type(**arguments)
            elif tool_name == "get_directory_stats":
                return await self._get_directory_stats(**arguments)
            elif tool_name == "identify_project_type":
                return await self._identify_project_type(**arguments)
            elif tool_name == "get_common_patterns":
                return await self._get_common_patterns(**arguments)
            else:
                raise ValueError(f"Unknown tool: {tool_name}")
        except Exception as e:
            return await self.handle_error(e, f"Tool call failed: {tool_name}")
    
    async def _get_repository_tree(self, repository: str, branch: str = "main",
                                  max_depth: int = 5, include_files: bool = True) -> Dict[str, Any]:
        """
        Get complete directory tree structure.
        """
        if not await self.check_rate_limit():
            return {"error": "Rate limit exceeded"}
        
        try:
            repo = self._get_repository(repository)
            
            def build_tree(path: str = "", depth: int = 0) -> Dict[str, Any]:
                if depth > max_depth:
                    return None
                
                try:
                    contents = repo.get_contents(path, ref=branch)
                    
                    tree = {
                        "path": path or "/",
                        "type": "directory",
                        "children": []
                    }
                    
                    for item in contents:
                        if item.type == "dir":
                            child_tree = build_tree(item.path, depth + 1)
                            if child_tree:
                                tree["children"].append(child_tree)
                        elif include_files and item.type == "file":
                            tree["children"].append({
                                "path": item.path,
                                "name": item.name,
                                "type": "file",
                                "size": item.size,
                                "sha": item.sha
                            })
                    
                    return tree
                    
                except Exception as e:
                    self.logger.warning(f"Error building tree for path {path}: {e}")
                    return None
            
            tree = build_tree()
            
            return {
                "repository": repository,
                "branch": branch,
                "max_depth": max_depth,
                "include_files": include_files,
                "tree": tree
            }
            
        except Exception as e:
            return await self.handle_error(e, f"get_repository_tree({repository}, {branch})")
    
    async def _analyze_structure(self, repository: str, branch: str = "main") -> Dict[str, Any]:
        """
        Analyze repository structure patterns.
        """
        if not await self.check_rate_limit():
            return {"error": "Rate limit exceeded"}
        
        try:
            repo = self._get_repository(repository)
            
            # Get all files and directories
            all_files = []
            all_dirs = []
            
            def collect_items(path: str = ""):
                try:
                    contents = repo.get_contents(path, ref=branch)
                    for item in contents:
                        if item.type == "file":
                            all_files.append(item)
                        elif item.type == "dir":
                            all_dirs.append(item)
                            collect_items(item.path)
                except Exception as e:
                    self.logger.warning(f"Error collecting items for path {path}: {e}")
            
            collect_items()
            
            # Analyze structure patterns
            analysis = {
                "repository": repository,
                "branch": branch,
                "total_files": len(all_files),
                "total_directories": len(all_dirs),
                "file_types": {},
                "directory_patterns": {},
                "config_files": [],
                "structure_analysis": {}
            }
            
            # Analyze file types
            for file in all_files:
                ext = Path(file.name).suffix.lower()
                if ext:
                    analysis["file_types"][ext] = analysis["file_types"].get(ext, 0) + 1
            
            # Find configuration files
            for file in all_files:
                if self._is_config_file(file.name):
                    analysis["config_files"].append({
                        "name": file.name,
                        "path": file.path,
                        "size": file.size
                    })
            
            # Analyze directory patterns
            for directory in all_dirs:
                dir_name = Path(directory.path).name
                pattern = self._categorize_directory(dir_name)
                analysis["directory_patterns"][pattern] = analysis["directory_patterns"].get(pattern, 0) + 1
            
            # Structure analysis
            analysis["structure_analysis"] = {
                "has_src_directory": any("src" in d.path.lower() for d in all_dirs),
                "has_tests_directory": any("test" in d.path.lower() for d in all_dirs),
                "has_docs_directory": any("doc" in d.path.lower() for d in all_dirs),
                "has_config_directory": any("config" in d.path.lower() for d in all_dirs),
                "max_depth": max(len(Path(d.path).parts) for d in all_dirs) if all_dirs else 0,
                "average_files_per_directory": len(all_files) / len(all_dirs) if all_dirs else 0
            }
            
            return analysis
            
        except Exception as e:
            return await self.handle_error(e, f"analyze_structure({repository}, {branch})")
    
    async def _find_files_by_type(self, repository: str, file_extensions: Optional[List[str]] = None,
                                 file_types: Optional[List[str]] = None, branch: str = "main",
                                 recursive: bool = True) -> Dict[str, Any]:
        """
        Find files by extension or type.
        """
        if not await self.check_rate_limit():
            return {"error": "Rate limit exceeded"}
        
        try:
            repo = self._get_repository(repository)
            
            matching_files = []
            
            def search_files(path: str = ""):
                try:
                    contents = repo.get_contents(path, ref=branch)
                    for item in contents:
                        if item.type == "file":
                            # Check file extensions
                            if file_extensions:
                                ext = Path(item.name).suffix.lower()
                                if ext not in file_extensions:
                                    continue
                            
                            # Check file types
                            if file_types:
                                file_category = self._get_file_category(item.name)
                                if file_category not in file_types:
                                    continue
                            
                            matching_files.append({
                                "name": item.name,
                                "path": item.path,
                                "size": item.size,
                                "sha": item.sha,
                                "url": item.html_url
                            })
                        elif recursive and item.type == "dir":
                            search_files(item.path)
                            
                except Exception as e:
                    self.logger.warning(f"Error searching files in path {path}: {e}")
            
            search_files()
            
            return {
                "repository": repository,
                "branch": branch,
                "file_extensions": file_extensions,
                "file_types": file_types,
                "recursive": recursive,
                "total_matches": len(matching_files),
                "files": matching_files
            }
            
        except Exception as e:
            return await self.handle_error(e, f"find_files_by_type({repository}, {branch})")
    
    async def _get_directory_stats(self, repository: str, directory_path: str = "",
                                  branch: str = "main") -> Dict[str, Any]:
        """
        Get directory statistics.
        """
        if not await self.check_rate_limit():
            return {"error": "Rate limit exceeded"}
        
        try:
            repo = self._get_repository(repository)
            
            stats = {
                "directory_path": directory_path or "/",
                "repository": repository,
                "branch": branch,
                "files": [],
                "directories": [],
                "file_types": {},
                "total_size": 0,
                "largest_files": []
            }
            
            def analyze_directory(path: str):
                try:
                    contents = repo.get_contents(path, ref=branch)
                    
                    for item in contents:
                        if item.type == "file":
                            stats["files"].append({
                                "name": item.name,
                                "path": item.path,
                                "size": item.size,
                                "sha": item.sha
                            })
                            stats["total_size"] += item.size
                            
                            # Track file types
                            ext = Path(item.name).suffix.lower()
                            if ext:
                                stats["file_types"][ext] = stats["file_types"].get(ext, 0) + 1
                                
                        elif item.type == "dir":
                            stats["directories"].append({
                                "name": item.name,
                                "path": item.path,
                                "sha": item.sha
                            })
                            
                except Exception as e:
                    self.logger.warning(f"Error analyzing directory {path}: {e}")
            
            analyze_directory(directory_path)
            
            # Find largest files
            stats["largest_files"] = sorted(
                stats["files"], 
                key=lambda x: x["size"], 
                reverse=True
            )[:10]
            
            stats["total_files"] = len(stats["files"])
            stats["total_directories"] = len(stats["directories"])
            
            return stats
            
        except Exception as e:
            return await self.handle_error(e, f"get_directory_stats({repository}, {directory_path})")
    
    async def _identify_project_type(self, repository: str, branch: str = "main") -> Dict[str, Any]:
        """
        Identify project type based on structure.
        """
        if not await self.check_rate_limit():
            return {"error": "Rate limit exceeded"}
        
        try:
            repo = self._get_repository(repository)
            
            # Get root directory contents
            contents = repo.get_contents("", ref=branch)
            
            project_indicators = {
                "python": ["requirements.txt", "setup.py", "pyproject.toml", "Pipfile", "poetry.lock"],
                "javascript": ["package.json", "yarn.lock", "package-lock.json"],
                "java": ["pom.xml", "build.gradle", "gradle.properties"],
                "csharp": [".csproj", ".sln", "packages.config"],
                "go": ["go.mod", "go.sum"],
                "rust": ["Cargo.toml", "Cargo.lock"],
                "php": ["composer.json", "composer.lock"],
                "ruby": ["Gemfile", "Gemfile.lock", "Rakefile"],
                "docker": ["Dockerfile", "docker-compose.yml", ".dockerignore"],
                "kubernetes": ["kustomization.yaml", "helm-chart", "deployment.yaml"],
                "terraform": ["*.tf", "*.tfvars", "terraform.tfstate"],
                "ansible": ["playbook.yml", "inventory", "roles/"],
                "documentation": ["README.md", "docs/", "*.md"],
                "testing": ["tests/", "test/", "spec/", "cypress/", "jest.config.js"]
            }
            
            found_indicators = {}
            confidence_scores = {}
            
            for project_type, indicators in project_indicators.items():
                found_indicators[project_type] = []
                score = 0
                
                for indicator in indicators:
                    # Check for exact matches
                    for item in contents:
                        if item.name == indicator:
                            found_indicators[project_type].append(indicator)
                            score += 1
                        elif indicator.endswith("/") and item.type == "dir" and item.name == indicator[:-1]:
                            found_indicators[project_type].append(indicator)
                            score += 1
                        elif indicator.startswith("*.") and item.name.endswith(indicator[1:]):
                            found_indicators[project_type].append(indicator)
                            score += 0.5
                
                confidence_scores[project_type] = score
            
            # Determine primary project type
            primary_type = max(confidence_scores.items(), key=lambda x: x[1])
            
            return {
                "repository": repository,
                "branch": branch,
                "primary_type": primary_type[0] if primary_type[1] > 0 else "unknown",
                "confidence_score": primary_type[1],
                "found_indicators": found_indicators,
                "confidence_scores": confidence_scores,
                "all_indicators": {k: v for k, v in confidence_scores.items() if v > 0}
            }
            
        except Exception as e:
            return await self.handle_error(e, f"identify_project_type({repository}, {branch})")
    
    async def _get_common_patterns(self, repository: str, branch: str = "main",
                                  pattern_type: str = "all") -> Dict[str, Any]:
        """
        Find common patterns in repository.
        """
        if not await self.check_rate_limit():
            return {"error": "Rate limit exceeded"}
        
        try:
            repo = self._get_repository(repository)
            
            patterns = {
                "naming_patterns": {},
                "structure_patterns": {},
                "file_patterns": {}
            }
            
            # Get all files and directories
            all_items = []
            
            def collect_all_items(path: str = ""):
                try:
                    contents = repo.get_contents(path, ref=branch)
                    for item in contents:
                        all_items.append(item)
                        if item.type == "dir":
                            collect_all_items(item.path)
                except Exception as e:
                    self.logger.warning(f"Error collecting items for path {path}: {e}")
            
            collect_all_items()
            
            # Analyze naming patterns
            if pattern_type in ["naming", "all"]:
                for item in all_items:
                    name = item.name
                    
                    # Check for common naming conventions
                    if re.match(r'^[a-z][a-z0-9_]*$', name):
                        patterns["naming_patterns"]["snake_case"] = patterns["naming_patterns"].get("snake_case", 0) + 1
                    elif re.match(r'^[A-Z][a-zA-Z0-9]*$', name):
                        patterns["naming_patterns"]["pascal_case"] = patterns["naming_patterns"].get("pascal_case", 0) + 1
                    elif re.match(r'^[a-z][a-zA-Z0-9]*$', name):
                        patterns["naming_patterns"]["camel_case"] = patterns["naming_patterns"].get("camel_case", 0) + 1
                    elif re.match(r'^[A-Z][A-Z0-9_]*$', name):
                        patterns["naming_patterns"]["screaming_snake_case"] = patterns["naming_patterns"].get("screaming_snake_case", 0) + 1
            
            # Analyze structure patterns
            if pattern_type in ["structure", "all"]:
                directories = [item for item in all_items if item.type == "dir"]
                for directory in directories:
                    dir_name = directory.name.lower()
                    
                    if "src" in dir_name or "source" in dir_name:
                        patterns["structure_patterns"]["source_directories"] = patterns["structure_patterns"].get("source_directories", 0) + 1
                    elif "test" in dir_name or "spec" in dir_name:
                        patterns["structure_patterns"]["test_directories"] = patterns["structure_patterns"].get("test_directories", 0) + 1
                    elif "doc" in dir_name or "docs" in dir_name:
                        patterns["structure_patterns"]["documentation_directories"] = patterns["structure_patterns"].get("documentation_directories", 0) + 1
                    elif "config" in dir_name or "conf" in dir_name:
                        patterns["structure_patterns"]["configuration_directories"] = patterns["structure_patterns"].get("configuration_directories", 0) + 1
            
            # Analyze file patterns
            if pattern_type in ["file", "all"]:
                files = [item for item in all_items if item.type == "file"]
                for file in files:
                    ext = Path(file.name).suffix.lower()
                    if ext:
                        patterns["file_patterns"][ext] = patterns["file_patterns"].get(ext, 0) + 1
            
            return {
                "repository": repository,
                "branch": branch,
                "pattern_type": pattern_type,
                "patterns": patterns
            }
            
        except Exception as e:
            return await self.handle_error(e, f"get_common_patterns({repository}, {branch})")
    
    def _is_config_file(self, file_path: str) -> bool:
        """
        Check if file is a configuration file.
        """
        config_patterns = [
            r'\.(config|conf|ini|yaml|yml|json|toml|xml)$',
            r'^(\.env|\.gitignore|\.dockerignore|\.editorconfig)',
            r'^(package\.json|requirements\.txt|setup\.py|pom\.xml|build\.gradle)',
            r'^(dockerfile|docker-compose\.yml|docker-compose\.yaml)',
            r'^(\.eslintrc|\.prettierrc|\.babelrc|\.browserslistrc)',
            r'^(tsconfig\.json|webpack\.config\.js|rollup\.config\.js)',
            r'^(\.travis\.yml|\.github/workflows/.*\.yml|\.gitlab-ci\.yml)'
        ]
        
        for pattern in config_patterns:
            if re.search(pattern, file_path, re.IGNORECASE):
                return True
        
        return False
    
    def _categorize_directory(self, dir_name: str) -> str:
        """
        Categorize directory by name.
        """
        dir_name_lower = dir_name.lower()
        
        if any(word in dir_name_lower for word in ["src", "source", "lib", "app"]):
            return "source_code"
        elif any(word in dir_name_lower for word in ["test", "spec", "tests"]):
            return "testing"
        elif any(word in dir_name_lower for word in ["doc", "docs", "documentation"]):
            return "documentation"
        elif any(word in dir_name_lower for word in ["config", "conf", "settings"]):
            return "configuration"
        elif any(word in dir_name_lower for word in ["build", "dist", "target", "out"]):
            return "build_output"
        elif any(word in dir_name_lower for word in ["assets", "static", "public", "media"]):
            return "assets"
        elif any(word in dir_name_lower for word in ["scripts", "tools", "bin"]):
            return "scripts"
        else:
            return "other"
    
    def _get_file_category(self, file_path: str) -> str:
        """
        Get file category based on extension and name.
        """
        ext = Path(file_path).suffix.lower()
        name = Path(file_path).name.lower()
        
        # Programming languages
        if ext in ['.py', '.pyx', '.pyi']:
            return 'python'
        elif ext in ['.js', '.jsx', '.ts', '.tsx']:
            return 'javascript'
        elif ext in ['.java', '.class']:
            return 'java'
        elif ext in ['.cs', '.vb']:
            return 'csharp'
        elif ext in ['.go']:
            return 'go'
        elif ext in ['.rs']:
            return 'rust'
        elif ext in ['.php']:
            return 'php'
        elif ext in ['.rb']:
            return 'ruby'
        elif ext in ['.cpp', '.cc', '.cxx', '.c']:
            return 'cpp'
        
        # Configuration files
        elif ext in ['.json', '.yaml', '.yml', '.toml', '.ini', '.cfg', '.conf']:
            return 'configuration'
        elif name in ['dockerfile', '.dockerignore'] or ext in ['.dockerfile']:
            return 'docker'
        
        # Documentation
        elif ext in ['.md', '.rst', '.txt', '.adoc']:
            return 'documentation'
        
        # Images
        elif ext in ['.png', '.jpg', '.jpeg', '.gif', '.svg', '.ico', '.bmp']:
            return 'image'
        
        # Data files
        elif ext in ['.csv', '.xml', '.sql', '.db', '.sqlite']:
            return 'data'
        
        # Archives
        elif ext in ['.zip', '.tar', '.gz', '.rar', '.7z']:
            return 'archive'
        
        else:
            return 'other' 