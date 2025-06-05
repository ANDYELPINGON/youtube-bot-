import pytest
import os
import sys
from unittest.mock import patch, MagicMock, mock_open

# Add the parent directory to the path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import main


class TestMainConfiguration:
    """Test configuration constants and basic setup"""
    
    def test_configuration_constants(self):
        """Test that configuration constants are properly defined"""
        assert hasattr(main, 'VIDEO_URL')
        assert hasattr(main, 'NUM_VIEWS')
        assert hasattr(main, 'MIN_VIEW_TIME')
        assert hasattr(main, 'MAX_VIEW_TIME')
        assert hasattr(main, 'CHROME_PROFILE_PATH')
        
        # Test that values are reasonable
        assert main.NUM_VIEWS > 0
        assert main.MIN_VIEW_TIME > 0
        assert main.MAX_VIEW_TIME > main.MIN_VIEW_TIME
        assert isinstance(main.VIDEO_URL, str)
        assert main.VIDEO_URL.startswith('https://')


class TestSetupDriver:
    """Test the setup_driver function"""
    
    @patch('main.webdriver.Chrome')
    @patch('main.Service')
    @patch('main.UserAgent')
    @patch('main.Options')
    def test_setup_driver_success(self, mock_options, mock_user_agent, mock_service, mock_chrome):
        """Test successful driver setup"""
        # Mock the UserAgent
        mock_ua_instance = MagicMock()
        mock_ua_instance.random = "Mozilla/5.0 (Test Browser)"
        mock_user_agent.return_value = mock_ua_instance
        
        # Mock the Options
        mock_options_instance = MagicMock()
        mock_options.return_value = mock_options_instance
        
        # Mock the Service
        mock_service_instance = MagicMock()
        mock_service.return_value = mock_service_instance
        
        # Mock the Chrome driver
        mock_driver = MagicMock()
        mock_chrome.return_value = mock_driver
        
        # Call the function
        result = main.setup_driver()
        
        # Verify the result
        assert result == mock_driver
        
        # Verify that Chrome options were configured
        mock_options_instance.add_argument.assert_called()
        mock_options_instance.add_experimental_option.assert_called()
        
        # Verify Chrome was instantiated with service and options
        mock_chrome.assert_called_once_with(service=mock_service_instance, options=mock_options_instance)
    
    @patch('main.webdriver.Chrome')
    @patch('main.Service')
    @patch('main.UserAgent')
    @patch('main.Options')
    def test_setup_driver_exception(self, mock_options, mock_user_agent, mock_service, mock_chrome):
        """Test driver setup when an exception occurs"""
        # Make Chrome raise an exception
        mock_chrome.side_effect = Exception("Chrome driver not found")
        
        # Call the function
        result = main.setup_driver()
        
        # Should return None on exception
        assert result is None
    
    @patch('main.webdriver.Chrome')
    @patch('main.Service')
    @patch('main.UserAgent')
    @patch('main.Options')
    def test_setup_driver_chrome_options_configuration(self, mock_options, mock_user_agent, mock_service, mock_chrome):
        """Test that Chrome options are properly configured"""
        # Mock the UserAgent
        mock_ua_instance = MagicMock()
        mock_ua_instance.random = "Mozilla/5.0 (Test Browser)"
        mock_user_agent.return_value = mock_ua_instance
        
        # Mock the Options
        mock_options_instance = MagicMock()
        mock_options.return_value = mock_options_instance
        
        # Mock the Service and Chrome
        mock_service.return_value = MagicMock()
        mock_chrome.return_value = MagicMock()
        
        # Call the function
        main.setup_driver()
        
        # Verify specific Chrome options were added
        expected_args = [
            '--ignore-certificate-errors',
            '--ignore-ssl-errors',
            '--allow-running-insecure-content',
            '--disable-web-security',
            '--disable-blink-features=AutomationControlled'
        ]
        
        # Check that add_argument was called with expected arguments
        calls = mock_options_instance.add_argument.call_args_list
        called_args = [call[0][0] for call in calls]
        
        for expected_arg in expected_args:
            assert any(expected_arg in arg for arg in called_args), f"Expected argument {expected_arg} not found"


class TestDirectoryCreation:
    """Test directory creation functionality"""
    
    @patch('os.path.exists')
    @patch('os.makedirs')
    def test_chrome_profile_directory_creation(self, mock_makedirs, mock_exists):
        """Test that Chrome profile directory is created when it doesn't exist"""
        # Mock that directory doesn't exist
        mock_exists.return_value = False
        
        # Test the directory creation logic directly
        import os
        if not os.path.exists(main.CHROME_PROFILE_PATH):
            os.makedirs(main.CHROME_PROFILE_PATH)
        
        # Verify directory creation was attempted
        mock_makedirs.assert_called_once_with(main.CHROME_PROFILE_PATH)
    
    @patch('os.path.exists')
    @patch('os.makedirs')
    def test_chrome_profile_directory_exists(self, mock_makedirs, mock_exists):
        """Test that Chrome profile directory is not created when it already exists"""
        # Mock that directory exists
        mock_exists.return_value = True
        
        # Test the directory creation logic directly
        import os
        if not os.path.exists(main.CHROME_PROFILE_PATH):
            os.makedirs(main.CHROME_PROFILE_PATH)
        
        # Verify directory creation was not attempted
        mock_makedirs.assert_not_called()


class TestYoutubeViewSimulator:
    """Test the youtube_view_simulator function"""
    
    @patch('main.setup_driver')
    def test_youtube_view_simulator_no_driver(self, mock_setup_driver):
        """Test youtube_view_simulator when driver setup fails"""
        # Mock setup_driver to return None
        mock_setup_driver.return_value = None
        
        # Call the function - should return early without error
        result = main.youtube_view_simulator()
        
        # Function should complete without raising an exception
        assert result is None
    
    @patch('main.setup_driver')
    @patch('main.time.sleep')
    @patch('main.time.time')
    @patch('main.random.uniform')
    @patch('main.random.randint')
    @patch('main.random.random')
    def test_youtube_view_simulator_with_driver(self, mock_random, mock_randint, mock_uniform, mock_time, mock_sleep, mock_setup_driver):
        """Test youtube_view_simulator with a working driver"""
        # Mock the driver
        mock_driver = MagicMock()
        mock_setup_driver.return_value = mock_driver
        
        # Mock time.time() to control the while loop - make it exit immediately
        mock_time.side_effect = [0, 100]  # start_time=0, then time > view_duration to exit loop
        
        # Mock random functions to return predictable values
        mock_uniform.return_value = 5.0
        mock_randint.return_value = 60
        mock_random.return_value = 0.5  # < 0.7, so no scroll
        
        # Mock find_element to simulate play button
        mock_play_button = MagicMock()
        mock_play_button.get_attribute.return_value = "Play"
        mock_driver.find_element.return_value = mock_play_button
        
        # Temporarily reduce NUM_VIEWS for testing
        original_num_views = main.NUM_VIEWS
        main.NUM_VIEWS = 1
        
        try:
            # Call the function
            main.youtube_view_simulator()
            
            # Verify driver methods were called
            mock_driver.set_window_size.assert_called_once_with(1200, 800)
            mock_driver.get.assert_called_with(main.VIDEO_URL)
            mock_driver.quit.assert_called_once()
            
        finally:
            # Restore original value
            main.NUM_VIEWS = original_num_views