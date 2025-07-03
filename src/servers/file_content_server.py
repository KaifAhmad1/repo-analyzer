"""
File Content Server using FastMCP for content retrieval and analysis from GitHub repositories
"""

import base64
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
mcp = FastMCP("File Content Server 📁")

class CodeAnalyzer:
    """Advanced code analysis for Python files"""
    
    @staticmethod
    def analyze_python_file(content: str) -> Dict[str, Any]:
        """Analyze Python file content using AST"""
        if not AST_AVAILABLE:
            return {"error": "AST analysis not available"}
        
        try:
            tree = ast.parse(content)
            analyzer = CodeAnalyzer()
            return analyzer._extract_analysis(tree, content)
        except Exception as e:
            return {"error": f"AST parsing failed: {str(e)}"}
    
    def _extract_analysis(self, tree: ast.AST, content: str) -> Dict[str, Any]:
        """Extract comprehensive analysis from AST"""
        analysis = {
            "functions": [],
            "classes": [],
            "imports": [],
            "variables": [],
            "calls": [],
            "complexity": 0,
            "metrics": self._calculate_metrics(content),
            "structure": self._analyze_structure(tree)
        }
        
        # Analyze each node type
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
            elif isinstance(node, ast.Assign):
                var_info = self._analyze_assignment(node)
                analysis["variables"].extend(var_info)
            elif isinstance(node, ast.Call):
                call_info = self._analyze_call(node)
                analysis["calls"].append(call_info)
        
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
            "decorators": [self._get_decorator_name(d) for d in node.decorator_list],
            "complexity": complexity,
            "lineno": getattr(node, 'lineno', 0),
            "end_lineno": getattr(node, 'end_lineno', 0),
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
            "bases": [self._get_name(base) for base in node.bases],
            "methods": methods,
            "lineno": getattr(node, 'lineno', 0),
            "end_lineno": getattr(node, 'end_lineno', 0),
            "has_docstring": ast.get_docstring(node) is not None
        }
    
    def _analyze_import(self, node: Union[ast.Import, ast.ImportFrom]) -> Dict[str, Any]:
        """Analyze import statement"""
        if isinstance(node, ast.Import):
            return {
                "type": "import",
                "modules": [alias.name for alias in node.names],
                "lineno": getattr(node, 'lineno', 0)
            }
        else:
            return {
                "type": "from_import",
                "module": node.module,
                "names": [alias.name for alias in node.names],
                "lineno": getattr(node, 'lineno', 0)
            }
    
    def _analyze_assignment(self, node: ast.Assign) -> List[Dict[str, Any]]:
        """Analyze assignment statement"""
        variables = []
        for target in node.targets:
            if isinstance(target, ast.Name):
                variables.append({
                    "name": target.id,
                    "lineno": getattr(node, 'lineno', 0)
                })
        return variables
    
    def _analyze_call(self, node: ast.Call) -> Dict[str, Any]:
        """Analyze function call"""
        return {
            "func": self._get_name(node.func),
            "args_count": len(node.args),
            "keywords": [kw.arg for kw in node.keywords],
            "lineno": getattr(node, 'lineno', 0)
        }
    
    def _calculate_metrics(self, content: str) -> Dict[str, Any]:
        """Calculate code metrics"""
        lines = content.split('\n')
        return {
            "total_lines": len(lines),
            "code_lines": len([line for line in lines if line.strip() and not line.strip().startswith('#')]),
            "comment_lines": len([line for line in lines if line.strip().startswith('#')]),
            "blank_lines": len([line for line in lines if not line.strip()]),
            "max_line_length": max(len(line) for line in lines) if lines else 0
        }
    
    def _analyze_structure(self, tree: ast.AST) -> Dict[str, Any]:
        """Analyze code structure"""
        return {
            "nesting_depth": self._calculate_nesting_depth(tree),
            "has_main_block": self._has_main_block(tree),
            "has_async_code": self._has_async_code(tree)
        }
    
    def _calculate_nesting_depth(self, tree: ast.AST) -> int:
        """Calculate maximum nesting depth"""
        max_depth = 0
        current_depth = 0
        
        for node in ast.walk(tree):
            if isinstance(node, (ast.If, ast.For, ast.While, ast.Try, ast.With)):
                current_depth += 1
                max_depth = max(max_depth, current_depth)
            elif isinstance(node, ast.FunctionDef):
                current_depth += 1
                max_depth = max(max_depth, current_depth)
        
        return max_depth
    
    def _has_main_block(self, tree: ast.AST) -> bool:
        """Check if file has main block"""
        for node in ast.walk(tree):
            if isinstance(node, ast.If) and isinstance(node.test, ast.Compare):
                if isinstance(node.test.left, ast.Name) and node.test.left.id == "__name__":
                    return True
        return False
    
    def _has_async_code(self, tree: ast.AST) -> bool:
        """Check if file has async code"""
        for node in ast.walk(tree):
            if isinstance(node, (ast.AsyncFunctionDef, ast.AsyncFor, ast.AsyncWith)):
                return True
        return False
    
    def _get_name(self, node: ast.AST) -> str:
        """Extract name from AST node"""
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            return f"{self._get_name(node.value)}.{node.attr}"
        return str(node)
    
    def _get_decorator_name(self, node: ast.AST) -> str:
        """Extract decorator name"""
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Call):
            return self._get_name(node.func)
        return str(node)

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

@mcp.tool
async def get_file_content(repo_url: str, file_path: str, ctx: Context) -> Dict[str, Any]:
    """Get content of a specific file in a GitHub repository"""
    try:
        await ctx.info(f"Fetching file: {file_path} from {repo_url}")
        
        owner, repo = parse_repo_url(repo_url)
        api_url = f"/repos/{owner}/{repo}/contents/{file_path}"
        file_data = make_github_request(api_url)
        
        # Handle different content encodings
        encoding = file_data.get("encoding", "")
        if encoding == "base64":
            content = base64.b64decode(file_data["content"]).decode("utf-8", errors="ignore")
        else:
            content = file_data["content"]
        
        result = {
            "content": content,
            "encoding": encoding,
            "size": file_data.get("size", 0),
            "path": file_path,
            "sha": file_data.get("sha", ""),
            "url": file_data.get("html_url", ""),
            "success": True
        }
        
        await ctx.info(f"Successfully retrieved {file_path} ({len(content)} characters)")
        return result
        
    except Exception as e:
        await ctx.error(f"Error fetching file {file_path}: {str(e)}")
        return {
            "error": str(e),
            "path": file_path,
            "success": False
        }

@mcp.tool
async def list_directory(repo_url: str, path: str = "", ctx: Context = None) -> Dict[str, Any]:
    """List contents of a directory in a GitHub repository"""
    try:
        if ctx:
            await ctx.info(f"Listing directory: {path or 'root'} from {repo_url}")
        
        owner, repo = parse_repo_url(repo_url)
        api_url = f"/repos/{owner}/{repo}/contents/{path}"
        contents = make_github_request(api_url)
        
        files = []
        directories = []
        
        for item in contents:
            if item["type"] == "file":
                files.append({
                    "name": item["name"],
                    "path": item["path"],
                    "size": item["size"],
                    "type": "file",
                    "url": item.get("html_url", "")
                })
            elif item["type"] == "dir":
                directories.append({
                    "name": item["name"],
                    "path": item["path"],
                    "type": "directory",
                    "url": item.get("html_url", "")
                })
        
        result = {
            "path": path or "root",
            "files": files,
            "directories": directories,
            "total_files": len(files),
            "total_directories": len(directories),
            "success": True
        }
        
        if ctx:
            await ctx.info(f"Found {len(files)} files and {len(directories)} directories")
        
        return result
        
    except Exception as e:
        error_msg = f"Error listing directory {path}: {str(e)}"
        if ctx:
            await ctx.error(error_msg)
        return {
            "error": str(e),
            "path": path,
            "success": False
        }

@mcp.tool
async def get_readme_content(repo_url: str, ctx: Context) -> Dict[str, Any]:
    """Get README content from a GitHub repository"""
    try:
        await ctx.info(f"Fetching README from {repo_url}")
        
        owner, repo = parse_repo_url(repo_url)
        
        # Try different README file names
        readme_files = ["README.md", "README.txt", "README.rst", "readme.md"]
        
        for readme_file in readme_files:
            try:
                api_url = f"/repos/{owner}/{repo}/contents/{readme_file}"
                file_data = make_github_request(api_url)
                
                encoding = file_data.get("encoding", "")
                if encoding == "base64":
                    content = base64.b64decode(file_data["content"]).decode("utf-8", errors="ignore")
                else:
                    content = file_data["content"]
                
                result = {
                    "content": content,
                    "filename": readme_file,
                    "size": file_data.get("size", 0),
                    "url": file_data.get("html_url", ""),
                    "success": True
                }
                
                await ctx.info(f"Found README: {readme_file}")
                return result
                
            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 404:
                    continue  # Try next README file
                else:
                    raise
        
        # No README found
        await ctx.info("No README file found")
        return {
            "error": "No README file found",
            "success": False
        }
        
    except Exception as e:
        await ctx.error(f"Error fetching README: {str(e)}")
        return {
            "error": str(e),
            "success": False
        }

@mcp.tool
async def get_file_info(repo_url: str, file_path: str, ctx: Context) -> Dict[str, Any]:
    """Get detailed information about a file without downloading content"""
    try:
        await ctx.info(f"Getting file info: {file_path}")
        
        owner, repo = parse_repo_url(repo_url)
        api_url = f"/repos/{owner}/{repo}/contents/{file_path}"
        file_data = make_github_request(api_url)
        
        result = {
            "name": file_data["name"],
            "path": file_data["path"],
            "size": file_data.get("size", 0),
            "type": file_data["type"],
            "sha": file_data.get("sha", ""),
            "url": file_data.get("html_url", ""),
            "download_url": file_data.get("download_url", ""),
            "encoding": file_data.get("encoding", ""),
            "success": True
        }
        
        await ctx.info(f"File info retrieved: {file_path} ({file_data.get('size', 0)} bytes)")
        return result
        
    except Exception as e:
        await ctx.error(f"Error getting file info: {str(e)}")
        return {
            "error": str(e),
            "path": file_path,
            "success": False
        }

@mcp.tool
async def analyze_file_content(repo_url: str, file_path: str, ctx: Context) -> Dict[str, Any]:
    """Get file content with advanced code analysis for Python files"""
    try:
        await ctx.info(f"Analyzing file content: {file_path}")
        
        # Get file content first
        content_result = await get_file_content(repo_url, file_path, ctx)
        if not content_result.get("success"):
            return content_result
        
        content = content_result["content"]
        
        # Check if it's a Python file for analysis
        if file_path.endswith('.py'):
            code_analysis = CodeAnalyzer.analyze_python_file(content)
        else:
            code_analysis = {"note": "Code analysis only available for Python files"}
        
        result = {
            "file_path": file_path,
            "content": content,
            "size": content_result.get("size", 0),
            "url": content_result.get("url", ""),
            "code_analysis": code_analysis,
            "success": True
        }
        
        await ctx.info(f"File analysis completed for {file_path}")
        return result
        
    except Exception as e:
        await ctx.error(f"Error analyzing file content: {str(e)}")
        return {
            "error": str(e),
            "file_path": file_path,
            "success": False
        }

@mcp.tool
async def get_code_summary(repo_url: str, file_path: str, ctx: Context) -> Dict[str, Any]:
    """Get a summary of code structure and metrics for Python files"""
    try:
        await ctx.info(f"Generating code summary for {file_path}")
        
        # Get file content
        content_result = await get_file_content(repo_url, file_path, ctx)
        if not content_result.get("success"):
            return content_result
        
        content = content_result["content"]
        
        if not file_path.endswith('.py'):
            return {
                "error": "Code summary only available for Python files",
                "file_path": file_path,
                "success": False
            }
        
        # Analyze the code
        analysis = CodeAnalyzer.analyze_python_file(content)
        
        # Create summary
        summary = {
            "file_path": file_path,
            "metrics": analysis.get("metrics", {}),
            "structure": {
                "functions": len(analysis.get("functions", [])),
                "classes": len(analysis.get("classes", [])),
                "imports": len(analysis.get("imports", [])),
                "complexity": analysis.get("complexity", 0),
                "nesting_depth": analysis.get("structure", {}).get("nesting_depth", 0),
                "has_async_code": analysis.get("structure", {}).get("has_async_code", False),
                "has_main_block": analysis.get("structure", {}).get("has_main_block", False)
            },
            "functions": [f["name"] for f in analysis.get("functions", [])],
            "classes": [c["name"] for c in analysis.get("classes", [])],
            "imports": [imp.get("modules", [imp.get("module", "")]) for imp in analysis.get("imports", [])],
            "success": True
        }
        
        await ctx.info(f"Code summary generated for {file_path}")
        return summary
        
    except Exception as e:
        await ctx.error(f"Error generating code summary: {str(e)}")
        return {
            "error": str(e),
            "file_path": file_path,
            "success": False
        }

@mcp.tool
async def find_code_issues(repo_url: str, file_path: str, ctx: Context) -> Dict[str, Any]:
    """Find potential code issues and suggestions for Python files"""
    try:
        await ctx.info(f"Analyzing code issues for {file_path}")
        
        # Get file content
        content_result = await get_file_content(repo_url, file_path, ctx)
        if not content_result.get("success"):
            return content_result
        
        content = content_result["content"]
        
        if not file_path.endswith('.py'):
            return {
                "error": "Code issue analysis only available for Python files",
                "file_path": file_path,
                "success": False
            }
        
        # Analyze the code
        analysis = CodeAnalyzer.analyze_python_file(content)
        
        # Find potential issues
        issues = []
        
        # Check for high complexity functions
        for func in analysis.get("functions", []):
            if func.get("complexity", 0) > 10:
                issues.append({
                    "type": "high_complexity",
                    "severity": "warning",
                    "message": f"Function '{func['name']}' has high complexity ({func['complexity']})",
                    "line": func.get("lineno", 0)
                })
        
        # Check for missing docstrings
        for func in analysis.get("functions", []):
            if not func.get("has_docstring", False):
                issues.append({
                    "type": "missing_docstring",
                    "severity": "info",
                    "message": f"Function '{func['name']}' lacks docstring",
                    "line": func.get("lineno", 0)
                })
        
        for cls in analysis.get("classes", []):
            if not cls.get("has_docstring", False):
                issues.append({
                    "type": "missing_docstring",
                    "severity": "info",
                    "message": f"Class '{cls['name']}' lacks docstring",
                    "line": cls.get("lineno", 0)
                })
        
        # Check for long lines
        metrics = analysis.get("metrics", {})
        if metrics.get("max_line_length", 0) > 100:
            issues.append({
                "type": "long_lines",
                "severity": "warning",
                "message": f"File has lines longer than 100 characters (max: {metrics['max_line_length']})",
                "line": 0
            })
        
        # Check for deep nesting
        structure = analysis.get("structure", {})
        if structure.get("nesting_depth", 0) > 5:
            issues.append({
                "type": "deep_nesting",
                "severity": "warning",
                "message": f"Code has deep nesting (depth: {structure['nesting_depth']})",
                "line": 0
            })
        
        result = {
            "file_path": file_path,
            "issues": issues,
            "issue_count": len(issues),
            "severity_counts": {
                "error": len([i for i in issues if i["severity"] == "error"]),
                "warning": len([i for i in issues if i["severity"] == "warning"]),
                "info": len([i for i in issues if i["severity"] == "info"])
            },
            "success": True
        }
        
        await ctx.info(f"Found {len(issues)} code issues in {file_path}")
        return result
        
    except Exception as e:
        await ctx.error(f"Error analyzing code issues: {str(e)}")
        return {
            "error": str(e),
            "file_path": file_path,
            "success": False
        }

# Resources for static data access
@mcp.resource("file://{owner}/{repo}/{path}")
def get_file_resource(owner: str, repo: str, path: str) -> Dict[str, Any]:
    """Resource endpoint for file content"""
    try:
        api_url = f"/repos/{owner}/{repo}/contents/{path}"
        file_data = make_github_request(api_url)
        
        encoding = file_data.get("encoding", "")
        if encoding == "base64":
            content = base64.b64decode(file_data["content"]).decode("utf-8", errors="ignore")
        else:
            content = file_data["content"]
        
        return {
            "content": content,
            "path": path,
            "size": file_data.get("size", 0)
        }
    except Exception as e:
        return {"error": str(e), "path": path}

@mcp.resource("directory://{owner}/{repo}/{path}")
def get_directory_resource(owner: str, repo: str, path: str) -> Dict[str, Any]:
    """Resource endpoint for directory listing"""
    try:
        api_url = f"/repos/{owner}/{repo}/contents/{path}"
        contents = make_github_request(api_url)
        
        files = [item for item in contents if item["type"] == "file"]
        directories = [item for item in contents if item["type"] == "dir"]
        
        return {
            "path": path,
            "files": files,
            "directories": directories,
            "total_files": len(files),
            "total_directories": len(directories)
        }
    except Exception as e:
        return {"error": str(e), "path": path}

# Prompts for common file operations
@mcp.prompt
def file_analysis_prompt(file_path: str, content: str) -> str:
    """Generate a prompt for analyzing file content"""
    return f"""Analyze the following file: {file_path}

Content:
{content[:2000]}{'...' if len(content) > 2000 else ''}

Please provide:
1. File type and purpose
2. Key components or functions
3. Dependencies or imports
4. Any notable patterns or issues"""

@mcp.prompt
def readme_analysis_prompt(content: str) -> str:
    """Generate a prompt for analyzing README content"""
    return f"""Analyze this README file:

{content[:3000]}{'...' if len(content) > 3000 else ''}

Please provide:
1. Project overview and purpose
2. Installation instructions
3. Usage examples
4. Key features
5. Dependencies or requirements"""

if __name__ == "__main__":
    mcp.run() 