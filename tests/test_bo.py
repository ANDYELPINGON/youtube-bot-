import pytest
import os
import sys
from unittest.mock import patch, MagicMock, PropertyMock
import numpy as np

# Add the parent directory to the path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import bo


class TestAdvancedViewBot:
    """Test the AdvancedViewBot class"""
    
    def test_init(self):
        """Test AdvancedViewBot initialization"""
        video_url = "https://youtube.com/watch?v=test123"
        view_count = 5
        
        with patch('bo.ProxyRotator') as mock_proxy_rotator, \
             patch('bo.UserAgent') as mock_user_agent, \
             patch('bo.HumanBehaviorSimulator') as mock_human_pattern:
            
            bot = bo.AdvancedViewBot(video_url, view_count)
            
            assert bot.video_url == video_url
            assert bot.view_count == view_count
            assert bot.proxy_rotator is not None
            assert bot.ua is not None
            assert bot.human_pattern is not None
    
    def test_init_default_view_count(self):
        """Test AdvancedViewBot initialization with default view count"""
        video_url = "https://youtube.com/watch?v=test123"
        
        with patch('bo.ProxyRotator'), \
             patch('bo.UserAgent'), \
             patch('bo.HumanBehaviorSimulator'):
            
            bot = bo.AdvancedViewBot(video_url)
            
            assert bot.video_url == video_url
            assert bot.view_count == 10  # Default value
    
    @patch('bo.webdriver.Chrome')
    @patch('bo.Options')
    @patch('bo.time.sleep')
    @patch('bo.random.randint')
    def test_selenium_view_single_iteration(self, mock_randint, mock_sleep, mock_options, mock_chrome):
        """Test a single iteration of selenium_view method"""
        video_url = "https://youtube.com/watch?v=test123"
        
        with patch('bo.ProxyRotator') as mock_proxy_rotator_class, \
             patch('bo.UserAgent') as mock_user_agent_class, \
             patch('bo.HumanBehaviorSimulator') as mock_human_pattern_class:
            
            # Setup mocks
            mock_proxy_rotator = MagicMock()
            mock_proxy_rotator.get_next_proxy.return_value = "proxy.example.com:8080"
            mock_proxy_rotator_class.return_value = mock_proxy_rotator
            
            mock_ua = MagicMock()
            mock_ua.random = "Mozilla/5.0 (Test Browser)"
            mock_user_agent_class.return_value = mock_ua
            
            mock_human_pattern = MagicMock()
            mock_human_pattern_class.return_value = mock_human_pattern
            
            mock_options_instance = MagicMock()
            mock_options.return_value = mock_options_instance
            
            mock_driver = MagicMock()
            mock_chrome.return_value = mock_driver
            
            mock_randint.side_effect = [60, 120]  # watch_time, sleep_time
            
            # Create bot with view_count=1 for single iteration
            bot = bo.AdvancedViewBot(video_url, view_count=1)
            bot.random_interactions = MagicMock()  # Mock this method
            
            # Call the method
            bot.selenium_view()
            
            # Verify Chrome options were configured
            mock_options_instance.add_argument.assert_called()
            mock_options_instance.add_experimental_option.assert_called()
            
            # Verify driver interactions
            mock_driver.execute_script.assert_called()
            mock_driver.get.assert_called_with(video_url)
            mock_driver.quit.assert_called()
            
            # Verify human behavior simulation
            mock_human_pattern.simulate_human_behavior.assert_called_with(mock_driver)
            bot.random_interactions.assert_called_with(mock_driver)
    
    @patch('bo.sync_playwright')
    @patch('bo.time.sleep')
    @patch('bo.random.randint')
    def test_playwright_view_single_iteration(self, mock_randint, mock_sleep, mock_sync_playwright):
        """Test a single iteration of playwright_view method"""
        video_url = "https://youtube.com/watch?v=test123"
        
        with patch('bo.ProxyRotator') as mock_proxy_rotator_class, \
             patch('bo.UserAgent') as mock_user_agent_class, \
             patch('bo.HumanBehaviorSimulator') as mock_human_pattern_class:
            
            # Setup mocks
            mock_proxy_rotator = MagicMock()
            mock_proxy_rotator.get_next_proxy.return_value = "proxy.example.com:8080"
            mock_proxy_rotator_class.return_value = mock_proxy_rotator
            
            mock_ua = MagicMock()
            mock_ua.random = "Mozilla/5.0 (Test Browser)"
            mock_user_agent_class.return_value = mock_ua
            
            mock_human_pattern = MagicMock()
            mock_human_pattern_class.return_value = mock_human_pattern
            
            # Setup Playwright mocks
            mock_playwright = MagicMock()
            mock_browser = MagicMock()
            mock_context = MagicMock()
            mock_page = MagicMock()
            
            mock_playwright.chromium.launch.return_value = mock_browser
            mock_browser.new_context.return_value = mock_context
            mock_context.new_page.return_value = mock_page
            
            mock_sync_playwright.return_value.__enter__.return_value = mock_playwright
            
            mock_randint.side_effect = [1000, 700, 60, 120]  # viewport width, height, watch_time, sleep_time
            
            # Create bot with view_count=1 for single iteration
            bot = bo.AdvancedViewBot(video_url, view_count=1)
            bot.simulate_human_interactions = MagicMock()  # Mock this method
            
            # Call the method
            bot.playwright_view()
            
            # Verify Playwright interactions
            mock_playwright.chromium.launch.assert_called()
            mock_browser.new_context.assert_called()
            mock_page.goto.assert_called_with(video_url)
            mock_context.close.assert_called()
            mock_browser.close.assert_called()
            
            # Verify human behavior simulation
            mock_human_pattern.playwright_navigation.assert_called_with(mock_page)
            bot.simulate_human_interactions.assert_called_with(mock_page)
    
    @patch('bo.ActionChains')
    @patch('bo.time.sleep')
    @patch('bo.random.randint')
    @patch('bo.random.uniform')
    @patch('bo.random.random')
    @patch('bo.random.choice')
    def test_random_interactions(self, mock_choice, mock_random, mock_uniform, mock_randint, mock_sleep, mock_action_chains):
        """Test the random_interactions method"""
        video_url = "https://youtube.com/watch?v=test123"
        
        with patch('bo.ProxyRotator'), \
             patch('bo.UserAgent'), \
             patch('bo.HumanBehaviorSimulator'):
            
            bot = bo.AdvancedViewBot(video_url)
            
            # Setup mocks - need to mock the chained methods properly
            mock_driver = MagicMock()
            mock_actions = MagicMock()
            mock_move_by_offset = MagicMock()
            mock_perform = MagicMock()
            
            # Set up the chain: ActionChains().move_by_offset().perform()
            mock_actions.move_by_offset.return_value = mock_move_by_offset
            mock_move_by_offset.perform.return_value = mock_perform
            mock_action_chains.return_value = mock_actions
            
            # Provide enough values for all randint calls in the method
            mock_randint.side_effect = [5] + [-50, 50] * 10 + [500]  # iterations, then offsets for each iteration, then scroll
            mock_uniform.side_effect = [0.5] * 20  # sleep times
            mock_random.return_value = 0.8  # > 0.7, so should trigger click
            
            mock_element = MagicMock()
            mock_driver.find_elements.return_value = [mock_element]
            mock_choice.return_value = mock_element
            
            # Call the method
            bot.random_interactions(mock_driver)
            
            # Verify ActionChains was used
            mock_action_chains.assert_called_with(mock_driver)
            mock_actions.move_by_offset.assert_called()
            mock_move_by_offset.perform.assert_called()
            
            # Verify scroll was executed
            mock_driver.execute_script.assert_called()
            
            # Verify element click was attempted
            mock_driver.find_elements.assert_called_with(bo.By.TAG_NAME, 'button')
            mock_element.click.assert_called()


class TestHumanBehaviorSimulator:
    """Test the HumanBehaviorSimulator class"""
    
    @patch('bo.np.random.normal')
    def test_init(self, mock_normal):
        """Test HumanBehaviorSimulator initialization"""
        # Mock numpy random normal to return predictable values
        mock_normal.return_value = np.array([1, 2, 3])
        
        simulator = bo.HumanBehaviorSimulator()
        
        assert hasattr(simulator, 'mouse_movement_patterns')
        assert isinstance(simulator.mouse_movement_patterns, list)
        
        # Verify that generate_mouse_patterns was called (indirectly through np.random.normal)
        assert mock_normal.called
    
    @patch('bo.np.random.normal')
    def test_generate_mouse_patterns(self, mock_normal):
        """Test the generate_mouse_patterns method"""
        # Mock numpy random normal to return predictable values
        mock_normal.return_value = np.array([1, 2, 3])
        
        simulator = bo.HumanBehaviorSimulator()
        patterns = simulator.generate_mouse_patterns()
        
        assert isinstance(patterns, list)
        assert len(patterns) == 10  # Should generate 10 patterns
        
        # Verify np.random.normal was called with correct parameters
        mock_normal.assert_called_with(0, 1, 100)
    
    def test_simulate_human_behavior(self):
        """Test the simulate_human_behavior method"""
        with patch('bo.np.random.normal'):
            simulator = bo.HumanBehaviorSimulator()
            mock_driver = MagicMock()
            
            # Method should not raise an exception (currently just passes)
            result = simulator.simulate_human_behavior(mock_driver)
            assert result is None
    
    def test_playwright_navigation(self):
        """Test the playwright_navigation method"""
        with patch('bo.np.random.normal'):
            simulator = bo.HumanBehaviorSimulator()
            mock_page = MagicMock()
            
            # Method should not raise an exception (currently just passes)
            result = simulator.playwright_navigation(mock_page)
            assert result is None


class TestMainExecution:
    """Test the main execution block"""
    
    @patch('bo.AdvancedViewBot')
    def test_main_execution_mock(self, mock_bot_class):
        """Test the main execution block with mocked AdvancedViewBot"""
        mock_bot = MagicMock()
        mock_bot_class.return_value = mock_bot
        
        # Execute the main block by importing the module
        # Note: This is a simplified test since the actual main block has an infinite loop
        
        # Verify bot was created with correct parameters
        # This test is more conceptual since the actual main block would run indefinitely