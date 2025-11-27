"""
Code Assistant Module for NOVA
Provides code generation, explanation, and debugging capabilities.
"""
import logging
from typing import Optional
from config import Config

logger = logging.getLogger(__name__)

class CodeAssistant:
    """Code generation and assistance using Cursor API or Groq."""
    
    def __init__(self):
        """Initialize code assistant."""
        self.cursor_api_key = getattr(Config, 'CURSOR_API_KEY', None)
        # For now, we'll use Groq for code generation
        # Cursor API integration can be added later if needed
        logger.info("Code Assistant initialized")
    
    def generate_code(self, prompt: str, language: str = "python") -> str:
        """
        Generate code based on a prompt.
        
        Args:
            prompt: Description of what code to generate
            language: Programming language (default: python)
        
        Returns:
            Generated code as string
        """
        try:
            # Enhanced prompt for code generation
            code_prompt = f"""Generate {language} code for the following request:
{prompt}

Requirements:
- Write clean, well-commented code
- Include error handling where appropriate
- Follow best practices for {language}
- Return only the code, no explanations unless asked

Code:"""
            
            logger.info(f"Generating {language} code for: {prompt[:50]}")
            return code_prompt
            
        except Exception as e:
            logger.error(f"Error generating code: {e}")
            return f"❌ Error generating code: {e}"
    
    def explain_code(self, code: str) -> str:
        """
        Explain what a piece of code does.
        
        Args:
            code: Code to explain
        
        Returns:
            Explanation of the code
        """
        try:
            explain_prompt = f"""Explain the following code in detail:
```python
{code}
```

Provide:
1. What the code does
2. How it works
3. Key concepts used
4. Potential improvements"""
            
            logger.info("Explaining code")
            return explain_prompt
            
        except Exception as e:
            logger.error(f"Error explaining code: {e}")
            return f"❌ Error explaining code: {e}"
    
    def debug_code(self, code: str, error: Optional[str] = None) -> str:
        """
        Help debug code issues.
        
        Args:
            code: Code with issues
            error: Error message if available
        
        Returns:
            Debugging suggestions
        """
        try:
            debug_prompt = f"""Debug the following code:
```python
{code}
```

{f'Error message: {error}' if error else 'No specific error provided.'}

Please:
1. Identify potential issues
2. Suggest fixes
3. Provide corrected code if possible"""
            
            logger.info("Debugging code")
            return debug_prompt
            
        except Exception as e:
            logger.error(f"Error debugging code: {e}")
            return f"❌ Error debugging code: {e}"
    
    def review_code(self, code: str) -> str:
        """
        Review code for best practices and improvements.
        
        Args:
            code: Code to review
        
        Returns:
            Code review with suggestions
        """
        try:
            review_prompt = f"""Review the following code for:
1. Code quality and best practices
2. Performance optimizations
3. Security issues
4. Readability and maintainability
5. Suggestions for improvement

```python
{code}
```"""
            
            logger.info("Reviewing code")
            return review_prompt
            
        except Exception as e:
            logger.error(f"Error reviewing code: {e}")
            return f"❌ Error reviewing code: {e}"

