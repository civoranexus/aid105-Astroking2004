import unittest
from unittest.mock import patch, MagicMock
import os
from src.models.ai_service import generate_chat_response

class TestAIService(unittest.IsolatedAsyncioTestCase):
    
    @patch("src.models.ai_service.genai")
    @patch("src.models.ai_service.GOOGLE_API_KEY", "test_api_key")
    async def test_generate_chat_response_success(self, mock_genai):
        """Test that the AI service generates a response correctly when API key is present."""
        # Setup mock client
        mock_client_instance = MagicMock()
        mock_genai.Client.return_value = mock_client_instance
        
        # Setup mock response object
        mock_response = MagicMock()
        mock_response.text = "Here is the scheme information."
        
        # Mock the async generate_content method
        async def async_return(*args, **kwargs):
            return mock_response
            
        mock_client_instance.aio.models.generate_content.side_effect = async_return
        
        # Test data
        query = "Tell me about schemes"
        schemes = [{"title": "Scheme A", "description": "Description A"}]
        
        # Execute
        result = await generate_chat_response(query, schemes)
        
        # Assertions
        self.assertEqual(result, "Here is the scheme information.")
        mock_genai.Client.assert_called_with(api_key="test_api_key")
        mock_client_instance.aio.models.generate_content.assert_called_once()

    @patch("src.models.ai_service.GOOGLE_API_KEY", None)
    async def test_generate_chat_response_no_key(self):
        """Test that the service handles missing API keys gracefully."""
        result = await generate_chat_response("Hello", [])
        self.assertIn("AI features are currently unavailable", result)

    @patch("src.models.ai_service.genai")
    @patch("src.models.ai_service.GOOGLE_API_KEY", "test_api_key")
    async def test_generate_chat_response_api_error(self, mock_genai):
        """Test that the service handles API errors gracefully."""
        # Setup mock client
        mock_client_instance = MagicMock()
        mock_genai.Client.return_value = mock_client_instance
        
        # Mock the async generate_content method to raise an exception
        async def async_raise(*args, **kwargs):
            raise Exception("API connection failed")
            
        mock_client_instance.aio.models.generate_content.side_effect = async_raise
        
        result = await generate_chat_response("Hello", [])
        self.assertEqual(result, "Error generating AI response: API connection failed")

if __name__ == "__main__":
    unittest.main()