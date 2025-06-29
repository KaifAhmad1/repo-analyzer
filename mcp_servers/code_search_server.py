"""
Code Search MCP Server

This server provides tools for searching and analyzing code patterns, functions,
classes, and other code elements in GitHub repositories.
"""

import re
from typing import Dict, List, Optional, Any
from pathlib import Path

from .base_server import BaseMCPServer

class CodeSearchServer(BaseMCPServer):
    """
    MCP Server for code search operations.
    
    Tools provided:
    - search_code: Search for code patterns and functions
    - find_functions: Find function definitions
    - find_classes: Find class definitions
    - search_imports: Find import statements
    - analyze_code_patterns: Analyze code patterns and structure
    - find_dependencies: Find dependency relationships
    """
    
    def __init__(self):
        super().__init__(
            name="code_search_server",
            description="Server for searching and analyzing code patterns in GitHub repositories"
        )
        
    async def initialize_tools(self) -> List[Dict[str, Any]]:
        """
        Initialize tools for code search operations.
        """
        tools = [
            {
                "name": "search_code",
                "description": "Search for specific code patterns or functions in the repository",
                "parameters": {
                    "repository": "string (required): Repository name in format 'owner/repo'",
                    "query": "string (required): Search query or pattern to find",
                    "file_type": "string (optional): Filter by file type (e.g., 'py', 'js')",
                    "case_sensitive": "boolean (optional): Case sensitive search, defaults to false",
                    "regex": "boolean (optional): Use regex pattern, defaults to false",
                    "limit": "integer (optional): Number of results to return, defaults to 10"
                }
            },
            {
                "name": "find_functions",
                "description": "Find function definitions in the repository",
                "parameters": {
                    "repository": "string (required): Repository name in format 'owner/repo'",
                    "function_name": "string (optional): Specific function name to find",
                    "file_type": "string (optional): Filter by file type",
                    "limit": "integer (optional): Number of results to return, defaults to 10"
                }
            },
            {
                "name": "find_classes",
                "description": "Find class definitions in the repository",
                "parameters": {
                    "repository": "string (required): Repository name in format 'owner/repo'",
                    "class_name": "string (optional): Specific class name to find",
                    "file_type": "string (optional): Filter by file type",
                    "limit": "integer (optional): Number of results to return, defaults to 10"
                }
            },
            {
                "name": "search_imports",
                "description": "Find import statements and dependencies",
                "parameters": {
                    "repository": "string (required): Repository name in format 'owner/repo'",
                    "module_name": "string (optional): Specific module to search for",
                    "file_type": "string (optional): Filter by file type",
                    "limit": "integer (optional): Number of results to return, defaults to 10"
                }
            },
            {
                "name": "analyze_code_patterns",
                "description": "Analyze code patterns and structure",
                "parameters": {
                    "repository": "string (required): Repository name in format 'owner/repo'",
                    "file_type": "string (optional): Filter by file type",
                    "pattern_type": "string (optional): Type of patterns to analyze ('functions', 'classes', 'imports', 'all')"
                }
            },
            {
                "name": "find_dependencies",
                "description": "Find dependency relationships between files",
                "parameters": {
                    "repository": "string (required): Repository name in format 'owner/repo'",
                    "file_path": "string (optional): Specific file to analyze",
                    "file_type": "string (optional): Filter by file type"
                }
            }
        ]
        return tools
    
    async def handle_tool_call(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """
        Handle code search tool calls.
        """
        try:
            if tool_name == "search_code":
                return await self._search_code(**arguments)
            elif tool_name == "find_functions":
                return await self._find_functions(**arguments)
            elif tool_name == "find_classes":
                return await self._find_classes(**arguments)
            elif tool_name == "search_imports":
                return await self._search_imports(**arguments)
            elif tool_name == "analyze_code_patterns":
                return await self._analyze_code_patterns(**arguments)
            elif tool_name == "find_dependencies":
                return await self._find_dependencies(**arguments)
            else:
                raise ValueError(f"Unknown tool: {tool_name}")
        except Exception as e:
            return await self.handle_error(e, f"Tool call failed: {tool_name}")
    
    async def _search_code(self, repository: str, query: str, file_type: Optional[str] = None,
                          case_sensitive: bool = False, regex: bool = False, 
                          limit: int = 10) -> Dict[str, Any]:
        """
        Search for code patterns in repository.
        """
        if not await self.check_rate_limit():
            return {"error": "Rate limit exceeded"}
        
        try:
            repo = self._get_repository(repository)
            
            # Build search query
            search_parts = [f"repo:{repository}"]
            
            if file_type:
                search_parts.append(f"filename:*.{file_type}")
            
            if regex:
                search_parts.append(f"\"{query}\"")
            else:
                search_parts.append(query)
            
            search_query = " ".join(search_parts)
            
            # Search code
            results = repo.search_code(search_query)
            
            matches = []
            for result in results:
                if len(matches) >= limit:
                    break
                
                # Get file content to extract context
                try:
                    file_content = result.decoded_content.decode('utf-8')
                    lines = file_content.split('\n')
                    
                    # Find matching lines
                    matching_lines = []
                    for i, line in enumerate(lines, 1):
                        if regex:
                            if re.search(query, line, flags=0 if case_sensitive else re.IGNORECASE):
                                matching_lines.append({
                                    "line_number": i,
                                    "content": line.strip(),
                                    "match": re.search(query, line, flags=0 if case_sensitive else re.IGNORECASE).group()
                                })
                        else:
                            search_term = query if case_sensitive else query.lower()
                            line_to_search = line if case_sensitive else line.lower()
                            if search_term in line_to_search:
                                start_pos = line_to_search.find(search_term)
                                matching_lines.append({
                                    "line_number": i,
                                    "content": line.strip(),
                                    "match_start": start_pos,
                                    "match_end": start_pos + len(search_term)
                                })
                    
                    matches.append({
                        "file_path": result.path,
                        "file_name": result.name,
                        "repository": repository,
                        "url": result.html_url,
                        "score": result.score if hasattr(result, 'score') else None,
                        "matching_lines": matching_lines[:5],  # Limit to 5 lines per file
                        "total_matches": len(matching_lines)
                    })
                    
                except Exception as e:
                    self.logger.warning(f"Error processing search result {result.path}: {e}")
                    continue
            
            return {
                "repository": repository,
                "search_query": search_query,
                "query": query,
                "file_type": file_type,
                "case_sensitive": case_sensitive,
                "regex": regex,
                "total_results": len(matches),
                "matches": matches
            }
            
        except Exception as e:
            return await self.handle_error(e, f"search_code({repository}, {query})")
    
    async def _find_functions(self, repository: str, function_name: Optional[str] = None,
                             file_type: Optional[str] = None, limit: int = 10) -> Dict[str, Any]:
        """
        Find function definitions in repository.
        """
        if not await self.check_rate_limit():
            return {"error": "Rate limit exceeded"}
        
        try:
            repo = self._get_repository(repository)
            
            # Build search query for function definitions
            search_parts = [f"repo:{repository}"]
            
            if file_type:
                search_parts.append(f"filename:*.{file_type}")
            
            if function_name:
                # Search for specific function
                if file_type == "py":
                    search_parts.append(f"def {function_name}")
                elif file_type == "js":
                    search_parts.append(f"function {function_name}")
                elif file_type == "java":
                    search_parts.append(f"public.*{function_name}")
                else:
                    search_parts.append(f"def {function_name}")
            else:
                # Search for function definitions
                if file_type == "py":
                    search_parts.append("def ")
                elif file_type == "js":
                    search_parts.append("function ")
                elif file_type == "java":
                    search_parts.append("public.*(")
                else:
                    search_parts.append("def ")
            
            search_query = " ".join(search_parts)
            
            # Search code
            results = repo.search_code(search_query)
            
            functions = []
            for result in results:
                if len(functions) >= limit:
                    break
                
                try:
                    file_content = result.decoded_content.decode('utf-8')
                    lines = file_content.split('\n')
                    
                    # Find function definitions
                    function_definitions = []
                    for i, line in enumerate(lines, 1):
                        line_stripped = line.strip()
                        
                        # Python function definition
                        if file_type == "py" and line_stripped.startswith("def "):
                            if not function_name or function_name in line_stripped:
                                function_definitions.append({
                                    "line_number": i,
                                    "definition": line_stripped,
                                    "function_name": self._extract_function_name(line_stripped, "python")
                                })
                        
                        # JavaScript function definition
                        elif file_type == "js" and ("function " in line_stripped or "=>" in line_stripped):
                            if not function_name or function_name in line_stripped:
                                function_definitions.append({
                                    "line_number": i,
                                    "definition": line_stripped,
                                    "function_name": self._extract_function_name(line_stripped, "javascript")
                                })
                        
                        # Java method definition
                        elif file_type == "java" and ("public " in line_stripped or "private " in line_stripped) and "(" in line_stripped:
                            if not function_name or function_name in line_stripped:
                                function_definitions.append({
                                    "line_number": i,
                                    "definition": line_stripped,
                                    "function_name": self._extract_function_name(line_stripped, "java")
                                })
                    
                    if function_definitions:
                        functions.append({
                            "file_path": result.path,
                            "file_name": result.name,
                            "repository": repository,
                            "url": result.html_url,
                            "functions": function_definitions[:5]  # Limit to 5 functions per file
                        })
                    
                except Exception as e:
                    self.logger.warning(f"Error processing function search result {result.path}: {e}")
                    continue
            
            return {
                "repository": repository,
                "function_name": function_name,
                "file_type": file_type,
                "total_results": len(functions),
                "functions": functions
            }
            
        except Exception as e:
            return await self.handle_error(e, f"find_functions({repository}, {function_name})")
    
    async def _find_classes(self, repository: str, class_name: Optional[str] = None,
                           file_type: Optional[str] = None, limit: int = 10) -> Dict[str, Any]:
        """
        Find class definitions in repository.
        """
        if not await self.check_rate_limit():
            return {"error": "Rate limit exceeded"}
        
        try:
            repo = self._get_repository(repository)
            
            # Build search query for class definitions
            search_parts = [f"repo:{repository}"]
            
            if file_type:
                search_parts.append(f"filename:*.{file_type}")
            
            if class_name:
                # Search for specific class
                if file_type == "py":
                    search_parts.append(f"class {class_name}")
                elif file_type == "js":
                    search_parts.append(f"class {class_name}")
                elif file_type == "java":
                    search_parts.append(f"class {class_name}")
                else:
                    search_parts.append(f"class {class_name}")
            else:
                # Search for class definitions
                search_parts.append("class ")
            
            search_query = " ".join(search_parts)
            
            # Search code
            results = repo.search_code(search_query)
            
            classes = []
            for result in results:
                if len(classes) >= limit:
                    break
                
                try:
                    file_content = result.decoded_content.decode('utf-8')
                    lines = file_content.split('\n')
                    
                    # Find class definitions
                    class_definitions = []
                    for i, line in enumerate(lines, 1):
                        line_stripped = line.strip()
                        
                        # Class definition patterns
                        if line_stripped.startswith("class "):
                            if not class_name or class_name in line_stripped:
                                class_definitions.append({
                                    "line_number": i,
                                    "definition": line_stripped,
                                    "class_name": self._extract_class_name(line_stripped)
                                })
                    
                    if class_definitions:
                        classes.append({
                            "file_path": result.path,
                            "file_name": result.name,
                            "repository": repository,
                            "url": result.html_url,
                            "classes": class_definitions[:5]  # Limit to 5 classes per file
                        })
                    
                except Exception as e:
                    self.logger.warning(f"Error processing class search result {result.path}: {e}")
                    continue
            
            return {
                "repository": repository,
                "class_name": class_name,
                "file_type": file_type,
                "total_results": len(classes),
                "classes": classes
            }
            
        except Exception as e:
            return await self.handle_error(e, f"find_classes({repository}, {class_name})")
    
    async def _search_imports(self, repository: str, module_name: Optional[str] = None,
                             file_type: Optional[str] = None, limit: int = 10) -> Dict[str, Any]:
        """
        Find import statements and dependencies.
        """
        if not await self.check_rate_limit():
            return {"error": "Rate limit exceeded"}
        
        try:
            repo = self._get_repository(repository)
            
            # Build search query for imports
            search_parts = [f"repo:{repository}"]
            
            if file_type:
                search_parts.append(f"filename:*.{file_type}")
            
            if module_name:
                # Search for specific module imports
                if file_type == "py":
                    search_parts.append(f"import {module_name}")
                elif file_type == "js":
                    search_parts.append(f"import.*{module_name}")
                elif file_type == "java":
                    search_parts.append(f"import.*{module_name}")
                else:
                    search_parts.append(f"import {module_name}")
            else:
                # Search for import statements
                search_parts.append("import ")
            
            search_query = " ".join(search_parts)
            
            # Search code
            results = repo.search_code(search_query)
            
            imports = []
            for result in results:
                if len(imports) >= limit:
                    break
                
                try:
                    file_content = result.decoded_content.decode('utf-8')
                    lines = file_content.split('\n')
                    
                    # Find import statements
                    import_statements = []
                    for i, line in enumerate(lines, 1):
                        line_stripped = line.strip()
                        
                        # Import patterns
                        if line_stripped.startswith("import ") or line_stripped.startswith("from "):
                            if not module_name or module_name in line_stripped:
                                import_statements.append({
                                    "line_number": i,
                                    "statement": line_stripped,
                                    "module": self._extract_module_name(line_stripped, file_type)
                                })
                    
                    if import_statements:
                        imports.append({
                            "file_path": result.path,
                            "file_name": result.name,
                            "repository": repository,
                            "url": result.html_url,
                            "imports": import_statements[:10]  # Limit to 10 imports per file
                        })
                    
                except Exception as e:
                    self.logger.warning(f"Error processing import search result {result.path}: {e}")
                    continue
            
            return {
                "repository": repository,
                "module_name": module_name,
                "file_type": file_type,
                "total_results": len(imports),
                "imports": imports
            }
            
        except Exception as e:
            return await self.handle_error(e, f"search_imports({repository}, {module_name})")
    
    async def _analyze_code_patterns(self, repository: str, file_type: Optional[str] = None,
                                   pattern_type: str = "all") -> Dict[str, Any]:
        """
        Analyze code patterns and structure.
        """
        if not await self.check_rate_limit():
            return {"error": "Rate limit exceeded"}
        
        try:
            repo = self._get_repository(repository)
            
            # Get all files of the specified type
            all_files = []
            
            def collect_files(path: str = ""):
                try:
                    contents = repo.get_contents(path, ref="main")
                    for item in contents:
                        if item.type == "file":
                            if not file_type or item.name.endswith(f".{file_type}"):
                                all_files.append(item)
                        elif item.type == "dir":
                            collect_files(item.path)
                except Exception as e:
                    self.logger.warning(f"Error collecting files for path {path}: {e}")
            
            collect_files()
            
            patterns = {
                "functions": [],
                "classes": [],
                "imports": [],
                "statistics": {}
            }
            
            total_files = len(all_files)
            total_lines = 0
            total_functions = 0
            total_classes = 0
            total_imports = 0
            
            for file in all_files[:50]:  # Limit to 50 files for performance
                try:
                    content = file.decoded_content.decode('utf-8')
                    lines = content.split('\n')
                    total_lines += len(lines)
                    
                    # Analyze patterns
                    for line in lines:
                        line_stripped = line.strip()
                        
                        # Count functions
                        if pattern_type in ["functions", "all"]:
                            if line_stripped.startswith("def "):
                                total_functions += 1
                                patterns["functions"].append({
                                    "file": file.path,
                                    "function": self._extract_function_name(line_stripped, file_type or "py")
                                })
                        
                        # Count classes
                        if pattern_type in ["classes", "all"]:
                            if line_stripped.startswith("class "):
                                total_classes += 1
                                patterns["classes"].append({
                                    "file": file.path,
                                    "class": self._extract_class_name(line_stripped)
                                })
                        
                        # Count imports
                        if pattern_type in ["imports", "all"]:
                            if line_stripped.startswith("import ") or line_stripped.startswith("from "):
                                total_imports += 1
                                patterns["imports"].append({
                                    "file": file.path,
                                    "import": self._extract_module_name(line_stripped, file_type or "py")
                                })
                    
                except Exception as e:
                    self.logger.warning(f"Error analyzing file {file.path}: {e}")
                    continue
            
            # Calculate statistics
            patterns["statistics"] = {
                "total_files": total_files,
                "total_lines": total_lines,
                "total_functions": total_functions,
                "total_classes": total_classes,
                "total_imports": total_imports,
                "average_lines_per_file": total_lines / total_files if total_files > 0 else 0,
                "average_functions_per_file": total_functions / total_files if total_files > 0 else 0,
                "average_classes_per_file": total_classes / total_files if total_files > 0 else 0
            }
            
            return {
                "repository": repository,
                "file_type": file_type,
                "pattern_type": pattern_type,
                "patterns": patterns
            }
            
        except Exception as e:
            return await self.handle_error(e, f"analyze_code_patterns({repository}, {file_type})")
    
    async def _find_dependencies(self, repository: str, file_path: Optional[str] = None,
                                file_type: Optional[str] = None) -> Dict[str, Any]:
        """
        Find dependency relationships between files.
        """
        if not await self.check_rate_limit():
            return {"error": "Rate limit exceeded"}
        
        try:
            repo = self._get_repository(repository)
            
            dependencies = {
                "file_dependencies": {},
                "module_dependencies": {},
                "external_dependencies": []
            }
            
            if file_path:
                # Analyze specific file
                try:
                    file = repo.get_contents(file_path)
                    content = file.decoded_content.decode('utf-8')
                    
                    deps = self._extract_dependencies(content, file_type or "py")
                    dependencies["file_dependencies"][file_path] = deps
                    
                except Exception as e:
                    self.logger.warning(f"Error analyzing file {file_path}: {e}")
            else:
                # Analyze all files of specified type
                all_files = []
                
                def collect_files(path: str = ""):
                    try:
                        contents = repo.get_contents(path, ref="main")
                        for item in contents:
                            if item.type == "file":
                                if not file_type or item.name.endswith(f".{file_type}"):
                                    all_files.append(item)
                            elif item.type == "dir":
                                collect_files(item.path)
                    except Exception as e:
                        self.logger.warning(f"Error collecting files for path {path}: {e}")
                
                collect_files()
                
                # Analyze first 20 files for performance
                for file in all_files[:20]:
                    try:
                        content = file.decoded_content.decode('utf-8')
                        deps = self._extract_dependencies(content, file_type or "py")
                        dependencies["file_dependencies"][file.path] = deps
                        
                    except Exception as e:
                        self.logger.warning(f"Error analyzing file {file.path}: {e}")
                        continue
            
            return {
                "repository": repository,
                "file_path": file_path,
                "file_type": file_type,
                "dependencies": dependencies
            }
            
        except Exception as e:
            return await self.handle_error(e, f"find_dependencies({repository}, {file_path})")
    
    def _extract_function_name(self, line: str, language: str) -> str:
        """Extract function name from function definition line."""
        if language == "python":
            # Python: def function_name(params):
            match = re.match(r'def\s+(\w+)', line)
            return match.group(1) if match else "unknown"
        elif language == "javascript":
            # JavaScript: function functionName(params) or const functionName = (params) =>
            match = re.match(r'(?:function\s+(\w+)|const\s+(\w+)\s*=|let\s+(\w+)\s*=|var\s+(\w+)\s*=)', line)
            return next((name for name in match.groups() if name), "unknown") if match else "unknown"
        elif language == "java":
            # Java: public/private/protected returnType functionName(params)
            match = re.search(r'(\w+)\s*\([^)]*\)\s*\{?$', line)
            return match.group(1) if match else "unknown"
        else:
            return "unknown"
    
    def _extract_class_name(self, line: str) -> str:
        """Extract class name from class definition line."""
        # Class definition: class ClassName(optional_inheritance):
        match = re.match(r'class\s+(\w+)', line)
        return match.group(1) if match else "unknown"
    
    def _extract_module_name(self, line: str, language: str) -> str:
        """Extract module name from import statement."""
        if language == "python":
            # Python: import module or from module import item
            if line.startswith("from "):
                match = re.match(r'from\s+(\w+)', line)
            else:
                match = re.match(r'import\s+(\w+)', line)
            return match.group(1) if match else "unknown"
        elif language == "javascript":
            # JavaScript: import {item} from 'module'
            match = re.search(r"from\s+['\"]([^'\"]+)['\"]", line)
            return match.group(1) if match else "unknown"
        elif language == "java":
            # Java: import package.module
            match = re.match(r'import\s+([\w.]+)', line)
            return match.group(1) if match else "unknown"
        else:
            return "unknown"
    
    def _extract_dependencies(self, content: str, language: str) -> Dict[str, Any]:
        """Extract dependencies from file content."""
        dependencies = {
            "imports": [],
            "functions": [],
            "classes": []
        }
        
        lines = content.split('\n')
        
        for line in lines:
            line_stripped = line.strip()
            
            # Extract imports
            if line_stripped.startswith(("import ", "from ")):
                module = self._extract_module_name(line_stripped, language)
                if module != "unknown":
                    dependencies["imports"].append(module)
            
            # Extract function definitions
            if line_stripped.startswith("def "):
                func_name = self._extract_function_name(line_stripped, language)
                if func_name != "unknown":
                    dependencies["functions"].append(func_name)
            
            # Extract class definitions
            if line_stripped.startswith("class "):
                class_name = self._extract_class_name(line_stripped)
                if class_name != "unknown":
                    dependencies["classes"].append(class_name)
        
        return dependencies 