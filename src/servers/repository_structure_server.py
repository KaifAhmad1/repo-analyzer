"""
Repository Structure Server using FastMCP v2
Advanced repository structure analysis with code parsing
"""

import requests
import ast
import json
from typing import Dict, Any, List, Optional, Union
from fastmcp import FastMCP, Context

# Code analysis imports
try:
    import asttokens
    import libcst as cst
    from libcst.metadata import MetadataWrapper, QualifiedNameProvider
    from tree_sitter import Language, Parser
    AST_AVAILABLE = True
except ImportError:
    AST_AVAILABLE = False

# Create FastMCP server instance
mcp = FastMCP("Repository Structure Server 🌳")

class RepositoryAnalyzer:
    """Advanced repository analysis with code parsing"""
    
    @staticmethod
    def analyze_python_files(files: List[Dict[str, Any]], owner: str, repo: str) -> Dict[str, Any]:
        """Analyze all Python files in the repository"""
        if not AST_AVAILABLE:
            return {"error": "AST analysis not available"}
        
        analysis = {
            "total_python_files": 0,
            "functions": [],
            "classes": [],
            "imports": [],
            "complexity_stats": {
                "total_complexity": 0,
                "avg_complexity": 0,
                "max_complexity": 0
            },
            "file_analysis": []
        }
        
        python_files = [f for f in files if f["name"].endswith('.py')]
        analysis["total_python_files"] = len(python_files)
        
        for file_info in python_files:
            try:
                # Get file content
                api_url = f"/repos/{owner}/{repo}/contents/{file_info['path']}"
                file_data = make_github_request(api_url)
                
                if file_data.get("encoding") == "base64":
                    import base64
                    content = base64.b64decode(file_data["content"]).decode("utf-8", errors="ignore")
                else:
                    content = file_data["content"]
                
                # Analyze the file
                file_analysis = RepositoryAnalyzer._analyze_single_file(content, file_info["path"])
                analysis["file_analysis"].append(file_analysis)
                
                # Aggregate statistics
                analysis["functions"].extend(file_analysis.get("functions", []))
                analysis["classes"].extend(file_analysis.get("classes", []))
                analysis["imports"].extend(file_analysis.get("imports", []))
                analysis["complexity_stats"]["total_complexity"] += file_analysis.get("complexity", 0)
                
            except Exception:
                continue
        
        # Calculate averages
        if analysis["total_python_files"] > 0:
            analysis["complexity_stats"]["avg_complexity"] = analysis["complexity_stats"]["total_complexity"] / analysis["total_python_files"]
            analysis["complexity_stats"]["max_complexity"] = max([f.get("complexity", 0) for f in analysis["file_analysis"]], default=0)
        
        return analysis
    
    @staticmethod
    def _analyze_single_file(content: str, file_path: str) -> Dict[str, Any]:
        """Analyze a single Python file"""
        try:
            tree = ast.parse(content)
            analyzer = RepositoryAnalyzer()
            return analyzer._extract_file_analysis(tree, content, file_path)
        except Exception as e:
            return {"error": f"AST parsing failed: {str(e)}", "file_path": file_path}
    
    def _extract_file_analysis(self, tree: ast.AST, content: str, file_path: str) -> Dict[str, Any]:
        """Extract analysis from a single file"""
        analysis = {
            "file_path": file_path,
            "functions": [],
            "classes": [],
            "imports": [],
            "complexity": 0,
            "metrics": self._calculate_file_metrics(content)
        }
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                func_info = self._analyze_function(node)
                analysis["functions"].append(func_info)
                analysis["complexity"] += func_info.get("complexity", 1)
            elif isinstance(node, ast.ClassDef):
                class_info = self._analyze_class(node)
                analysis["classes"].append(class_info)
            elif isinstance(node, (ast.Import, ast.ImportFrom)):
                import_info = self._analyze_import(node)
                analysis["imports"].append(import_info)
        
        return analysis
    
    def _analyze_function(self, node: ast.FunctionDef) -> Dict[str, Any]:
        """Analyze function definition"""
        complexity = 1
        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.For, ast.While, ast.ExceptHandler)):
                complexity += 1
        
        return {
            "name": node.name,
            "args": [arg.arg for arg in node.args.args],
            "complexity": complexity,
            "lineno": getattr(node, 'lineno', 0),
            "has_docstring": ast.get_docstring(node) is not None
        }
    
    def _analyze_class(self, node: ast.ClassDef) -> Dict[str, Any]:
        """Analyze class definition"""
        methods = []
        for item in node.body:
            if isinstance(item, ast.FunctionDef):
                methods.append(item.name)
        
        return {
            "name": node.name,
            "methods": methods,
            "lineno": getattr(node, 'lineno', 0),
            "has_docstring": ast.get_docstring(node) is not None
        }
    
    def _analyze_import(self, node: Union[ast.Import, ast.ImportFrom]) -> Dict[str, Any]:
        """Analyze import statement"""
        if isinstance(node, ast.Import):
            return {
                "type": "import",
                "modules": [alias.name for alias in node.names]
            }
        else:
            return {
                "type": "from_import",
                "module": node.module,
                "names": [alias.name for alias in node.names]
            }
    
    def _calculate_file_metrics(self, content: str) -> Dict[str, Any]:
        """Calculate file metrics"""
        lines = content.split('\n')
        return {
            "total_lines": len(lines),
            "code_lines": len([line for line in lines if line.strip() and not line.strip().startswith('#')]),
            "comment_lines": len([line for line in lines if line.strip().startswith('#')]),
            "blank_lines": len([line for line in lines if not line.strip()])
        }

def parse_repo_url(repo_url: str) -> tuple[str, str]:
    """Parse GitHub repository URL to get owner and repo name"""
    if "github.com" in repo_url:
        parts = repo_url.replace("https://github.com/", "").split("/")
        owner = parts[0]
        repo = parts[1].replace(".git", "")
        return owner, repo
    else:
        raise ValueError("Invalid GitHub URL")

def make_github_request(endpoint: str) -> Dict[str, Any]:
    """Make a GitHub API request with proper headers"""
    headers = {"Accept": "application/vnd.github.v3+json"}
    response = requests.get(f"https://api.github.com{endpoint}", headers=headers)
    response.raise_for_status()
    return response.json()

def get_directory_contents(owner: str, repo: str, path: str = "") -> List[Dict[str, Any]]:
    """Get contents of a directory recursively"""
    try:
        api_url = f"/repos/{owner}/{repo}/contents/{path}"
        contents = make_github_request(api_url)
        return contents
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            return []
        raise

def build_tree_structure(owner: str, repo: str, path: str = "", max_depth: int = 3, current_depth: int = 0) -> Dict[str, Any]:
    """Build a tree structure for a directory"""
    if current_depth >= max_depth:
        return {"type": "truncated", "path": path}
    
    try:
        contents = get_directory_contents(owner, repo, path)
        
        tree = {
            "path": path or "root",
            "type": "directory",
            "children": [],
            "file_count": 0,
            "dir_count": 0
        }
        
        for item in contents:
            if item["type"] == "file":
                tree["children"].append({
                    "name": item["name"],
                    "path": item["path"],
                    "type": "file",
                    "size": item.get("size", 0),
                    "url": item.get("html_url", "")
                })
                tree["file_count"] += 1
            elif item["type"] == "dir":
                child_tree = build_tree_structure(owner, repo, item["path"], max_depth, current_depth + 1)
                tree["children"].append(child_tree)
                tree["dir_count"] += 1
        
        return tree
        
    except Exception:
        return {"type": "error", "path": path}

@mcp.tool
async def get_directory_tree(repo_url: str, ctx: Context, max_depth: int = 3) -> Dict[str, Any]:
    """Get a tree structure of the repository directory"""
    try:
        await ctx.info(f"Building directory tree for {repo_url} (max depth: {max_depth})")
        
        owner, repo = parse_repo_url(repo_url)
        tree = build_tree_structure(owner, repo, "", max_depth)
        
        # Calculate totals
        total_files = count_files(tree)
        total_dirs = count_directories(tree)
        
        result = {
            "repository": f"{owner}/{repo}",
            "tree": tree,
            "statistics": {
                "total_files": total_files,
                "total_directories": total_dirs,
                "max_depth": max_depth
            },
            "success": True
        }
        
        await ctx.info(f"Tree built successfully: {total_files} files, {total_dirs} directories")
        return result
        
    except Exception as e:
        await ctx.error(f"Error building directory tree: {str(e)}")
        return {
            "error": str(e),
            "success": False
        }

def count_files(tree: Dict[str, Any]) -> int:
    """Count total files in tree structure"""
    count = 0
    if tree.get("type") == "file":
        return 1
    elif tree.get("type") == "directory":
        count += tree.get("file_count", 0)
        for child in tree.get("children", []):
            count += count_files(child)
    return count

def count_directories(tree: Dict[str, Any]) -> int:
    """Count total directories in tree structure"""
    count = 0
    if tree.get("type") == "directory":
        count += tree.get("dir_count", 0)
        for child in tree.get("children", []):
            count += count_directories(child)
    return count

@mcp.tool
async def get_file_structure(repo_url: str, ctx: Context) -> Dict[str, Any]:
    """Get a flat list of all files in the repository"""
    try:
        await ctx.info(f"Getting file structure for {repo_url}")
        
        owner, repo = parse_repo_url(repo_url)
        
        def get_all_files(path: str = "") -> List[Dict[str, Any]]:
            files = []
            try:
                contents = get_directory_contents(owner, repo, path)
                for item in contents:
                    if item["type"] == "file":
                        files.append({
                            "name": item["name"],
                            "path": item["path"],
                            "size": item.get("size", 0),
                            "url": item.get("html_url", "")
                        })
                    elif item["type"] == "dir":
                        files.extend(get_all_files(item["path"]))
            except Exception:
                pass
            return files
        
        all_files = get_all_files()
        
        # Group files by extension
        file_types = {}
        for file in all_files:
            ext = file["name"].split(".")[-1] if "." in file["name"] else "no_extension"
            if ext not in file_types:
                file_types[ext] = []
            file_types[ext].append(file)
        
        # Find important files
        important_files = []
        for file in all_files:
            name = file["name"].lower()
            if any(keyword in name for keyword in ["readme", "license", "requirements", "package.json", "setup.py", "main", "app", "index"]):
                important_files.append(file)
        
        result = {
            "repository": f"{owner}/{repo}",
            "total_files": len(all_files),
            "file_types": {ext: len(files) for ext, files in file_types.items()},
            "important_files": important_files,
            "all_files": all_files,
            "success": True
        }
        
        await ctx.info(f"File structure retrieved: {len(all_files)} total files")
        return result
        
    except Exception as e:
        await ctx.error(f"Error getting file structure: {str(e)}")
        return {
            "error": str(e),
            "success": False
        }

@mcp.tool
async def analyze_project_structure(repo_url: str, ctx: Context) -> Dict[str, Any]:
    """Analyze the project structure and identify key components"""
    try:
        await ctx.info(f"Analyzing project structure for {repo_url}")
        
        owner, repo = parse_repo_url(repo_url)
        
        # Get root directory contents
        root_contents = get_directory_contents(owner, repo, "")
        
        analysis = {
            "repository": f"{owner}/{repo}",
            "project_type": "unknown",
            "languages": [],
            "frameworks": [],
            "key_files": [],
            "structure_analysis": {}
        }
        
        # Analyze root files
        root_files = [item["name"] for item in root_contents if item["type"] == "file"]
        
        # Detect project type
        if "package.json" in root_files:
            analysis["project_type"] = "Node.js"
            analysis["frameworks"].append("Node.js")
        elif "requirements.txt" in root_files or "setup.py" in root_files or "pyproject.toml" in root_files:
            analysis["project_type"] = "Python"
            analysis["frameworks"].append("Python")
        elif "pom.xml" in root_files:
            analysis["project_type"] = "Java"
            analysis["frameworks"].append("Java")
        elif "Cargo.toml" in root_files:
            analysis["project_type"] = "Rust"
            analysis["frameworks"].append("Rust")
        elif "go.mod" in root_files:
            analysis["project_type"] = "Go"
            analysis["frameworks"].append("Go")
        
        # Detect common frameworks
        if "package.json" in root_files:
            analysis["frameworks"].extend(["npm", "yarn"])
        if "requirements.txt" in root_files:
            analysis["frameworks"].append("pip")
        if "dockerfile" in [f.lower() for f in root_files]:
            analysis["frameworks"].append("Docker")
        if ".github" in [item["name"] for item in root_contents if item["type"] == "dir"]:
            analysis["frameworks"].append("GitHub Actions")
        
        # Identify key files
        key_file_patterns = [
            "readme", "license", "requirements", "package.json", "setup.py", 
            "main", "app", "index", "config", "dockerfile", "makefile"
        ]
        
        for file in root_files:
            if any(pattern in file.lower() for pattern in key_file_patterns):
                analysis["key_files"].append(file)
        
        # Analyze directory structure
        directories = [item["name"] for item in root_contents if item["type"] == "dir"]
        
        structure_analysis = {
            "has_src": "src" in directories,
            "has_tests": any("test" in d.lower() for d in directories),
            "has_docs": any("doc" in d.lower() for d in directories),
            "has_config": any("config" in d.lower() for d in directories),
            "has_scripts": any("script" in d.lower() for d in directories),
            "has_assets": any("asset" in d.lower() for d in directories)
        }
        
        analysis["structure_analysis"] = structure_analysis
        
        # Get language statistics
        try:
            languages_data = make_github_request(f"/repos/{owner}/{repo}/languages")
            analysis["languages"] = list(languages_data.keys())
        except Exception:
            pass
        
        result = {
            "analysis": analysis,
            "success": True
        }
        
        await ctx.info(f"Project analysis complete: {analysis['project_type']} project")
        return result
        
    except Exception as e:
        await ctx.error(f"Error analyzing project structure: {str(e)}")
        return {
            "error": str(e),
            "success": False
        }

@mcp.tool
async def find_files_by_pattern(repo_url: str, pattern: str, ctx: Context) -> Dict[str, Any]:
    """Find files matching a specific pattern"""
    try:
        await ctx.info(f"Searching for files matching '{pattern}' in {repo_url}")
        
        owner, repo = parse_repo_url(repo_url)
        
        def search_files(path: str = "") -> List[Dict[str, Any]]:
            matching_files = []
            try:
                contents = get_directory_contents(owner, repo, path)
                for item in contents:
                    if item["type"] == "file":
                        if pattern.lower() in item["name"].lower():
                            matching_files.append({
                                "name": item["name"],
                                "path": item["path"],
                                "size": item.get("size", 0),
                                "url": item.get("html_url", "")
                            })
                    elif item["type"] == "dir":
                        matching_files.extend(search_files(item["path"]))
            except Exception:
                pass
            return matching_files
        
        matching_files = search_files()
        
        result = {
            "pattern": pattern,
            "repository": f"{owner}/{repo}",
            "matches": matching_files,
            "count": len(matching_files),
            "success": True
        }
        
        await ctx.info(f"Found {len(matching_files)} files matching '{pattern}'")
        return result
        
    except Exception as e:
        await ctx.error(f"Error searching for files: {str(e)}")
        return {
            "error": str(e),
            "pattern": pattern,
            "success": False
        }

@mcp.tool
async def analyze_codebase_structure(repo_url: str, ctx: Context) -> Dict[str, Any]:
    """Analyze the codebase structure with AST parsing for Python files"""
    try:
        await ctx.info(f"Analyzing codebase structure for {repo_url}")
        
        owner, repo = parse_repo_url(repo_url)
        
        # First get all files
        def get_all_files(path: str = "") -> List[Dict[str, Any]]:
            files = []
            try:
                contents = get_directory_contents(owner, repo, path)
                for item in contents:
                    if item["type"] == "file":
                        files.append({
                            "name": item["name"],
                            "path": item["path"],
                            "size": item.get("size", 0),
                            "url": item.get("html_url", "")
                        })
                    elif item["type"] == "dir":
                        files.extend(get_all_files(item["path"]))
            except Exception:
                pass
            return files
        
        all_files = get_all_files()
        
        # Analyze Python files
        code_analysis = RepositoryAnalyzer.analyze_python_files(all_files, owner, repo)
        
        # Group files by type
        file_types = {}
        for file in all_files:
            ext = file["name"].split(".")[-1] if "." in file["name"] else "no_extension"
            if ext not in file_types:
                file_types[ext] = []
            file_types[ext].append(file)
        
        # Find important files
        important_files = []
        for file in all_files:
            name = file["name"].lower()
            if any(keyword in name for keyword in ["readme", "license", "requirements", "package.json", "setup.py", "main", "app", "index"]):
                important_files.append(file)
        
        result = {
            "repository": f"{owner}/{repo}",
            "total_files": len(all_files),
            "file_types": {ext: len(files) for ext, files in file_types.items()},
            "important_files": important_files,
            "code_analysis": code_analysis,
            "success": True
        }
        
        await ctx.info(f"Codebase analysis completed: {len(all_files)} files, {code_analysis.get('total_python_files', 0)} Python files")
        return result
        
    except Exception as e:
        await ctx.error(f"Error analyzing codebase structure: {str(e)}")
        return {
            "error": str(e),
            "success": False
        }

# Resources for static data access
@mcp.resource("structure://{owner}/{repo}/tree")
def get_structure_tree_resource(owner: str, repo: str) -> Dict[str, Any]:
    """Resource endpoint for repository tree structure"""
    try:
        tree = build_tree_structure(owner, repo, "", 2)
        return {
            "repository": f"{owner}/{repo}",
            "tree": tree
        }
    except Exception as e:
        return {"error": str(e)}

@mcp.resource("structure://{owner}/{repo}/files")
def get_structure_files_resource(owner: str, repo: str) -> Dict[str, Any]:
    """Resource endpoint for flat file list"""
    try:
        def get_all_files(path: str = "") -> List[Dict[str, Any]]:
            files = []
            try:
                contents = get_directory_contents(owner, repo, path)
                for item in contents:
                    if item["type"] == "file":
                        files.append({
                            "name": item["name"],
                            "path": item["path"],
                            "size": item.get("size", 0)
                        })
                    elif item["type"] == "dir":
                        files.extend(get_all_files(item["path"]))
            except Exception:
                pass
            return files
        
        all_files = get_all_files()
        return {
            "repository": f"{owner}/{repo}",
            "files": all_files,
            "count": len(all_files)
        }
    except Exception as e:
        return {"error": str(e)}

# Prompts for structure analysis
@mcp.prompt
def structure_analysis_prompt(repo_url: str, structure_data: str) -> str:
    """Generate a prompt for analyzing repository structure"""
    return f"""Analyze the structure of this repository: {repo_url}

Structure Data:
{structure_data[:2000]}{'...' if len(structure_data) > 2000 else ''}

Please provide:
1. Project organization and architecture
2. Key directories and their purposes
3. File organization patterns
4. Development workflow insights
5. Potential improvements or issues"""

@mcp.prompt
def file_organization_prompt(file_list: str) -> str:
    """Generate a prompt for analyzing file organization"""
    return f"""Analyze this file organization:

{file_list[:2000]}{'...' if len(file_list) > 2000 else ''}

Please provide:
1. File naming conventions
2. Directory structure patterns
3. Code organization principles
4. Best practices being followed
5. Suggestions for improvement"""

if __name__ == "__main__":
    mcp.run() 