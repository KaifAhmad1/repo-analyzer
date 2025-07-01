"""
Code Search Server using FastMCP v2
Advanced code search and analysis with AST/CST parsing
"""

import requests
import re
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
mcp = FastMCP("Code Search Server 🔍")

# Initialize Tree-sitter parser
def init_tree_sitter():
    """Initialize Tree-sitter parser for Python"""
    if not AST_AVAILABLE:
        return None
    
    try:
        # Load Python language
        Language.build_library(
            'build/my-languages.so',
            ['tree_sitter_python']
        )
        PY_LANGUAGE = Language('build/my-languages.so', 'python')
        parser = Parser()
        parser.set_language(PY_LANGUAGE)
        return parser
    except Exception:
        return None

TREE_SITTER_PARSER = init_tree_sitter()

class ASTAnalyzer:
    """Advanced AST analysis for Python code"""
    
    @staticmethod
    def analyze_ast(code: str) -> Dict[str, Any]:
        """Analyze Python code using AST"""
        if not AST_AVAILABLE:
            return {"error": "AST analysis not available"}
        
        try:
            tree = ast.parse(code)
            analyzer = ASTAnalyzer()
            return analyzer._extract_ast_info(tree)
        except Exception as e:
            return {"error": f"AST parsing failed: {str(e)}"}
    
    def _extract_ast_info(self, tree: ast.AST) -> Dict[str, Any]:
        """Extract comprehensive information from AST"""
        info = {
            "functions": [],
            "classes": [],
            "imports": [],
            "variables": [],
            "calls": [],
            "complexity": 0
        }
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                func_info = self._analyze_function(node)
                info["functions"].append(func_info)
                info["complexity"] += func_info.get("complexity", 1)
            elif isinstance(node, ast.ClassDef):
                class_info = self._analyze_class(node)
                info["classes"].append(class_info)
            elif isinstance(node, (ast.Import, ast.ImportFrom)):
                import_info = self._analyze_import(node)
                info["imports"].append(import_info)
            elif isinstance(node, ast.Assign):
                var_info = self._analyze_assignment(node)
                info["variables"].extend(var_info)
            elif isinstance(node, ast.Call):
                call_info = self._analyze_call(node)
                info["calls"].append(call_info)
        
        return info
    
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
            "end_lineno": getattr(node, 'end_lineno', 0)
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
            "end_lineno": getattr(node, 'end_lineno', 0)
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

class CSTAnalyzer:
    """Concrete Syntax Tree analysis for Python code"""
    
    @staticmethod
    def analyze_cst(code: str) -> Dict[str, Any]:
        """Analyze Python code using CST"""
        if not AST_AVAILABLE:
            return {"error": "CST analysis not available"}
        
        try:
            tree = cst.parse_module(code)
            wrapper = MetadataWrapper(tree)
            analyzer = CSTAnalyzer()
            return analyzer._extract_cst_info(tree, wrapper)
        except Exception as e:
            return {"error": f"CST parsing failed: {str(e)}"}
    
    def _extract_cst_info(self, tree: cst.Module, wrapper: MetadataWrapper) -> Dict[str, Any]:
        """Extract information from CST"""
        info = {
            "formatting": {},
            "comments": [],
            "whitespace": {},
            "structure": {}
        }
        
        # Analyze formatting
        info["formatting"] = self._analyze_formatting(tree)
        
        # Extract comments
        info["comments"] = self._extract_comments(tree)
        
        return info
    
    def _analyze_formatting(self, tree: cst.Module) -> Dict[str, Any]:
        """Analyze code formatting"""
        return {
            "indentation_style": "spaces",  # Could be detected
            "line_length": self._get_max_line_length(tree),
            "trailing_whitespace": self._check_trailing_whitespace(tree)
        }
    
    def _extract_comments(self, tree: cst.Module) -> List[Dict[str, Any]]:
        """Extract all comments from CST"""
        comments = []
        
        class CommentVisitor(cst.CSTVisitor):
            def visit_Comment(self, node: cst.Comment):
                comments.append({
                    "text": node.value,
                    "lineno": node.start_pos[0] if hasattr(node, 'start_pos') else 0
                })
        
        tree.visit(CommentVisitor())
        return comments
    
    def _get_max_line_length(self, tree: cst.Module) -> int:
        """Get maximum line length"""
        lines = tree.code.split('\n')
        return max(len(line) for line in lines) if lines else 0
    
    def _check_trailing_whitespace(self, tree: cst.Module) -> bool:
        """Check for trailing whitespace"""
        lines = tree.code.split('\n')
        return any(line.rstrip() != line for line in lines)

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
async def search_code(repo_url: str, query: str, ctx: Context, language: str = "") -> Dict[str, Any]:
    """Search for code patterns in repository"""
    try:
        await ctx.info(f"Searching for '{query}' in {repo_url}")
        
        owner, repo = parse_repo_url(repo_url)
        
        # Build search query
        search_query = f"{query} repo:{owner}/{repo}"
        if language:
            search_query += f" language:{language}"
        
        data = make_github_request(f"/search/code?q={search_query}&per_page=30")
        
        results = []
        for item in data.get("items", []):
            result = {
                "name": item["name"],
                "path": item["path"],
                "url": item["html_url"],
                "repository": item["repository"]["full_name"],
                "language": item.get("language", "Unknown"),
                "size": item.get("size", 0),
                "score": item.get("score", 0),
                "text_matches": []
            }
            
            # Extract text matches if available
            if "text_matches" in item:
                for match in item["text_matches"]:
                    result["text_matches"].append({
                        "fragment": match["fragment"],
                        "matches": [m["text"] for m in match.get("matches", [])]
                    })
            
            results.append(result)
        
        result = {
            "query": query,
            "repository": f"{owner}/{repo}",
            "language": language,
            "results": results,
            "total_count": data.get("total_count", 0),
            "count": len(results),
            "success": True
        }
        
        await ctx.info(f"Found {len(results)} code matches for '{query}'")
        return result
        
    except Exception as e:
        await ctx.error(f"Error searching code: {str(e)}")
        return {
            "error": str(e),
            "query": query,
            "success": False
        }

@mcp.tool
async def search_files(repo_url: str, filename_pattern: str, ctx: Context) -> Dict[str, Any]:
    """Search for files by filename pattern"""
    try:
        await ctx.info(f"Searching for files matching '{filename_pattern}' in {repo_url}")
        
        owner, repo = parse_repo_url(repo_url)
        
        # Use GitHub's filename search
        search_query = f"filename:{filename_pattern} repo:{owner}/{repo}"
        data = make_github_request(f"/search/code?q={search_query}&per_page=50")
        
        results = []
        for item in data.get("items", []):
            result = {
                "name": item["name"],
                "path": item["path"],
                "url": item["html_url"],
                "language": item.get("language", "Unknown"),
                "size": item.get("size", 0),
                "type": "file"
            }
            results.append(result)
        
        result = {
            "pattern": filename_pattern,
            "repository": f"{owner}/{repo}",
            "results": results,
            "total_count": data.get("total_count", 0),
            "count": len(results),
            "success": True
        }
        
        await ctx.info(f"Found {len(results)} files matching '{filename_pattern}'")
        return result
        
    except Exception as e:
        await ctx.error(f"Error searching files: {str(e)}")
        return {
            "error": str(e),
            "pattern": filename_pattern,
            "success": False
        }

@mcp.tool
async def find_functions(repo_url: str, function_name: str, ctx: Context, language: str = "") -> Dict[str, Any]:
    """Find function definitions in the repository"""
    try:
        await ctx.info(f"Searching for function '{function_name}' in {repo_url}")
        
        owner, repo = parse_repo_url(repo_url)
        
        # Search for function definitions
        search_queries = [
            f"def {function_name} repo:{owner}/{repo}",
            f"function {function_name} repo:{owner}/{repo}",
            f"func {function_name} repo:{owner}/{repo}",
            f"class {function_name} repo:{owner}/{repo}"
        ]
        
        if language:
            for i, query in enumerate(search_queries):
                search_queries[i] += f" language:{language}"
        
        all_results = []
        for query in search_queries:
            try:
                data = make_github_request(f"/search/code?q={query}&per_page=20")
                for item in data.get("items", []):
                    result = {
                        "name": item["name"],
                        "path": item["path"],
                        "url": item["html_url"],
                        "language": item.get("language", "Unknown"),
                        "text_matches": []
                    }
                    
                    if "text_matches" in item:
                        for match in item["text_matches"]:
                            result["text_matches"].append({
                                "fragment": match["fragment"],
                                "matches": [m["text"] for m in match.get("matches", [])]
                            })
                    
                    all_results.append(result)
            except Exception:
                continue
        
        # Remove duplicates based on path
        unique_results = []
        seen_paths = set()
        for result in all_results:
            if result["path"] not in seen_paths:
                unique_results.append(result)
                seen_paths.add(result["path"])
        
        result = {
            "function_name": function_name,
            "repository": f"{owner}/{repo}",
            "language": language,
            "results": unique_results,
            "count": len(unique_results),
            "success": True
        }
        
        await ctx.info(f"Found {len(unique_results)} function definitions for '{function_name}'")
        return result
        
    except Exception as e:
        await ctx.error(f"Error finding functions: {str(e)}")
        return {
            "error": str(e),
            "function_name": function_name,
            "success": False
        }

@mcp.tool
async def get_code_metrics(repo_url: str, ctx: Context) -> Dict[str, Any]:
    """Get code metrics and statistics for the repository"""
    try:
        await ctx.info(f"Calculating code metrics for {repo_url}")
        
        owner, repo = parse_repo_url(repo_url)
        
        # Get repository languages
        languages_data = make_github_request(f"/repos/{owner}/{repo}/languages")
        
        # Get repository statistics
        repo_data = make_github_request(f"/repos/{owner}/{repo}")
        
        # Get recent commits for activity analysis
        commits_data = make_github_request(f"/repos/{owner}/{repo}/commits?per_page=100")
        
        # Calculate metrics
        total_language_bytes = sum(languages_data.values())
        language_percentages = {
            lang: (bytes_count / total_language_bytes) * 100 
            for lang, bytes_count in languages_data.items()
        }
        
        # Analyze commit activity
        recent_activity = len(commits_data)
        unique_authors = set()
        for commit in commits_data:
            author = commit.get("author", {}).get("login")
            if author:
                unique_authors.add(author)
        
        # Get file count estimate
        try:
            contents = make_github_request(f"/repos/{owner}/{repo}/contents")
            file_count = len([item for item in contents if item["type"] == "file"])
        except:
            file_count = 0
        
        metrics = {
            "repository": f"{owner}/{repo}",
            "languages": languages_data,
            "language_percentages": language_percentages,
            "primary_language": max(languages_data.items(), key=lambda x: x[1])[0] if languages_data else "Unknown",
            "total_size": repo_data.get("size", 0),
            "file_count": file_count,
            "stars": repo_data.get("stargazers_count", 0),
            "forks": repo_data.get("forks_count", 0),
            "issues": repo_data.get("open_issues_count", 0),
            "recent_commits": recent_activity,
            "unique_contributors": len(unique_authors),
            "last_updated": repo_data.get("updated_at", ""),
            "created_at": repo_data.get("created_at", ""),
            "archived": repo_data.get("archived", False),
            "fork": repo_data.get("fork", False)
        }
        
        result = {
            "metrics": metrics,
            "success": True
        }
        
        await ctx.info(f"Code metrics calculated: {len(languages_data)} languages, {recent_activity} recent commits")
        return result
        
    except Exception as e:
        await ctx.error(f"Error calculating code metrics: {str(e)}")
        return {
            "error": str(e),
            "success": False
        }

@mcp.tool
async def search_dependencies(repo_url: str, ctx: Context) -> Dict[str, Any]:
    """Search for dependency files and analyze dependencies"""
    try:
        await ctx.info(f"Searching for dependencies in {repo_url}")
        
        owner, repo = parse_repo_url(repo_url)
        
        # Common dependency file patterns
        dependency_files = [
            "requirements.txt", "package.json", "pom.xml", "build.gradle", 
            "Cargo.toml", "go.mod", "composer.json", "Gemfile", "pubspec.yaml"
        ]
        
        found_dependencies = []
        
        for dep_file in dependency_files:
            try:
                # Search for the dependency file
                search_query = f"filename:{dep_file} repo:{owner}/{repo}"
                data = make_github_request(f"/search/code?q={search_query}&per_page=5")
                
                for item in data.get("items", []):
                    found_dependencies.append({
                        "filename": dep_file,
                        "path": item["path"],
                        "url": item["html_url"],
                        "language": item.get("language", "Unknown"),
                        "size": item.get("size", 0)
                    })
            except Exception:
                continue
        
        # Group by dependency type
        dependency_types = {
            "Python": [f for f in found_dependencies if f["filename"] in ["requirements.txt", "setup.py", "pyproject.toml"]],
            "Node.js": [f for f in found_dependencies if f["filename"] in ["package.json", "yarn.lock", "package-lock.json"]],
            "Java": [f for f in found_dependencies if f["filename"] in ["pom.xml", "build.gradle", "gradle.properties"]],
            "Rust": [f for f in found_dependencies if f["filename"] in ["Cargo.toml", "Cargo.lock"]],
            "Go": [f for f in found_dependencies if f["filename"] in ["go.mod", "go.sum"]],
            "PHP": [f for f in found_dependencies if f["filename"] in ["composer.json", "composer.lock"]],
            "Ruby": [f for f in found_dependencies if f["filename"] in ["Gemfile", "Gemfile.lock"]],
            "Dart": [f for f in found_dependencies if f["filename"] in ["pubspec.yaml", "pubspec.lock"]]
        }
        
        result = {
            "repository": f"{owner}/{repo}",
            "dependency_files": found_dependencies,
            "dependency_types": dependency_types,
            "total_files": len(found_dependencies),
            "success": True
        }
        
        await ctx.info(f"Found {len(found_dependencies)} dependency files")
        return result
        
    except Exception as e:
        await ctx.error(f"Error searching dependencies: {str(e)}")
        return {
            "error": str(e),
            "success": False
        }

@mcp.tool
async def analyze_code_structure(repo_url: str, file_path: str, ctx: Context) -> Dict[str, Any]:
    """Analyze code structure using AST and CST for Python files"""
    try:
        await ctx.info(f"Analyzing code structure for {file_path}")
        
        # First get the file content
        owner, repo = parse_repo_url(repo_url)
        api_url = f"/repos/{owner}/{repo}/contents/{file_path}"
        file_data = make_github_request(api_url)
        
        if file_data.get("encoding") == "base64":
            import base64
            content = base64.b64decode(file_data["content"]).decode("utf-8", errors="ignore")
        else:
            content = file_data["content"]
        
        # Check if it's a Python file
        if not file_path.endswith('.py'):
            return {
                "error": "AST/CST analysis only available for Python files",
                "file_path": file_path,
                "success": False
            }
        
        # Perform AST analysis
        ast_analysis = ASTAnalyzer.analyze_ast(content)
        
        # Perform CST analysis
        cst_analysis = CSTAnalyzer.analyze_cst(content)
        
        # Calculate additional metrics
        metrics = {
            "total_lines": len(content.split('\n')),
            "code_lines": len([line for line in content.split('\n') if line.strip() and not line.strip().startswith('#')]),
            "comment_lines": len([line for line in content.split('\n') if line.strip().startswith('#')]),
            "blank_lines": len([line for line in content.split('\n') if not line.strip()]),
            "function_count": len(ast_analysis.get("functions", [])),
            "class_count": len(ast_analysis.get("classes", [])),
            "import_count": len(ast_analysis.get("imports", [])),
            "complexity_score": ast_analysis.get("complexity", 0)
        }
        
        result = {
            "file_path": file_path,
            "ast_analysis": ast_analysis,
            "cst_analysis": cst_analysis,
            "metrics": metrics,
            "success": True
        }
        
        await ctx.info(f"Code analysis completed for {file_path}")
        return result
        
    except Exception as e:
        await ctx.error(f"Error analyzing code structure: {str(e)}")
        return {
            "error": str(e),
            "file_path": file_path,
            "success": False
        }

@mcp.tool
async def find_code_patterns(repo_url: str, pattern_type: str, ctx: Context, language: str = "Python") -> Dict[str, Any]:
    """Find specific code patterns using AST analysis"""
    try:
        await ctx.info(f"Searching for {pattern_type} patterns in {repo_url}")
        
        owner, repo = parse_repo_url(repo_url)
        
        # Search for Python files
        search_query = f"language:python repo:{owner}/{repo}"
        data = make_github_request(f"/search/code?q={search_query}&per_page=50")
        
        patterns = []
        for item in data.get("items", []):
            try:
                # Get file content
                file_path = item["path"]
                file_data = make_github_request(f"/repos/{owner}/{repo}/contents/{file_path}")
                
                if file_data.get("encoding") == "base64":
                    import base64
                    content = base64.b64decode(file_data["content"]).decode("utf-8", errors="ignore")
                else:
                    content = file_data["content"]
                
                # Analyze based on pattern type
                if pattern_type == "async_functions":
                    found_patterns = _find_async_patterns(content)
                elif pattern_type == "decorators":
                    found_patterns = _find_decorator_patterns(content)
                elif pattern_type == "type_hints":
                    found_patterns = _find_type_hint_patterns(content)
                elif pattern_type == "exceptions":
                    found_patterns = _find_exception_patterns(content)
                else:
                    found_patterns = []
                
                if found_patterns:
                    patterns.append({
                        "file_path": file_path,
                        "url": item["html_url"],
                        "patterns": found_patterns
                    })
                    
            except Exception:
                continue
        
        result = {
            "pattern_type": pattern_type,
            "repository": f"{owner}/{repo}",
            "files_with_patterns": patterns,
            "count": len(patterns),
            "success": True
        }
        
        await ctx.info(f"Found {len(patterns)} files with {pattern_type} patterns")
        return result
        
    except Exception as e:
        await ctx.error(f"Error finding code patterns: {str(e)}")
        return {
            "error": str(e),
            "pattern_type": pattern_type,
            "success": False
        }

def _find_async_patterns(content: str) -> List[Dict[str, Any]]:
    """Find async function patterns"""
    patterns = []
    try:
        tree = ast.parse(content)
        for node in ast.walk(tree):
            if isinstance(node, ast.AsyncFunctionDef):
                patterns.append({
                    "type": "async_function",
                    "name": node.name,
                    "lineno": getattr(node, 'lineno', 0)
                })
            elif isinstance(node, ast.AsyncFor):
                patterns.append({
                    "type": "async_for",
                    "lineno": getattr(node, 'lineno', 0)
                })
            elif isinstance(node, ast.AsyncWith):
                patterns.append({
                    "type": "async_with",
                    "lineno": getattr(node, 'lineno', 0)
                })
    except:
        pass
    return patterns

def _find_decorator_patterns(content: str) -> List[Dict[str, Any]]:
    """Find decorator patterns"""
    patterns = []
    try:
        tree = ast.parse(content)
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.decorator_list:
                for decorator in node.decorator_list:
                    patterns.append({
                        "type": "decorator",
                        "function": node.name,
                        "decorator": ASTAnalyzer()._get_decorator_name(decorator),
                        "lineno": getattr(node, 'lineno', 0)
                    })
    except:
        pass
    return patterns

def _find_type_hint_patterns(content: str) -> List[Dict[str, Any]]:
    """Find type hint patterns"""
    patterns = []
    try:
        tree = ast.parse(content)
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.returns:
                patterns.append({
                    "type": "return_type_hint",
                    "function": node.name,
                    "return_type": ASTAnalyzer()._get_name(node.returns),
                    "lineno": getattr(node, 'lineno', 0)
                })
            elif isinstance(node, ast.arg) and node.annotation:
                patterns.append({
                    "type": "parameter_type_hint",
                    "parameter": node.arg,
                    "type_hint": ASTAnalyzer()._get_name(node.annotation),
                    "lineno": getattr(node, 'lineno', 0)
                })
    except:
        pass
    return patterns

def _find_exception_patterns(content: str) -> List[Dict[str, Any]]:
    """Find exception handling patterns"""
    patterns = []
    try:
        tree = ast.parse(content)
        for node in ast.walk(tree):
            if isinstance(node, ast.Try):
                patterns.append({
                    "type": "try_except",
                    "lineno": getattr(node, 'lineno', 0),
                    "except_count": len(node.handlers)
                })
            elif isinstance(node, ast.Raise):
                patterns.append({
                    "type": "raise",
                    "lineno": getattr(node, 'lineno', 0)
                })
    except:
        pass
    return patterns

# Resources for static data access
@mcp.resource("search://{owner}/{repo}/languages")
def get_languages_resource(owner: str, repo: str) -> Dict[str, Any]:
    """Resource endpoint for repository languages"""
    try:
        languages_data = make_github_request(f"/repos/{owner}/{repo}/languages")
        return {
            "repository": f"{owner}/{repo}",
            "languages": languages_data
        }
    except Exception as e:
        return {"error": str(e)}

@mcp.resource("search://{owner}/{repo}/metrics")
def get_metrics_resource(owner: str, repo: str) -> Dict[str, Any]:
    """Resource endpoint for basic repository metrics"""
    try:
        repo_data = make_github_request(f"/repos/{owner}/{repo}")
        return {
            "repository": f"{owner}/{repo}",
            "stars": repo_data.get("stargazers_count", 0),
            "forks": repo_data.get("forks_count", 0),
            "issues": repo_data.get("open_issues_count", 0),
            "size": repo_data.get("size", 0),
            "language": repo_data.get("language", "Unknown"),
            "updated_at": repo_data.get("updated_at", "")
        }
    except Exception as e:
        return {"error": str(e)}

# Prompts for code analysis
@mcp.prompt
def code_search_prompt(query: str, results: str) -> str:
    """Generate a prompt for analyzing code search results"""
    return f"""Analyze these code search results for '{query}':

{results[:3000]}{'...' if len(results) > 3000 else ''}

Please provide:
1. Most relevant matches and their significance
2. Code patterns and implementations found
3. File organization and structure insights
4. Potential improvements or issues
5. Usage patterns and best practices"""

@mcp.prompt
def dependency_analysis_prompt(dependencies: str) -> str:
    """Generate a prompt for analyzing dependencies"""
    return f"""Analyze these project dependencies:

{dependencies[:2000]}{'...' if len(dependencies) > 2000 else ''}

Please provide:
1. Technology stack and frameworks used
2. Dependency management approach
3. Potential security or version issues
4. Modernization opportunities
5. Best practices recommendations"""

if __name__ == "__main__":
    mcp.run()