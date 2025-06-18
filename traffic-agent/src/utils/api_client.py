"""
Cliente para las APIs externas de optimización.
"""
import requests
import json
from typing import Dict, Any, Optional
from flask import current_app

class ApiClient:
    """Client for interacting with optimization APIs."""
    
    @staticmethod
    def call_standard_optimizer(weights: Dict[str, float]) -> Dict[str, Any]:
        """
        Call the standard optimization service.
        
        Args:
            weights: Dictionary with normalized weights
            
        Returns:
            API response as dictionary
        """
        url = current_app.config['STANDARD_OPTIMIZER_URL']
        timeout = current_app.config['API_TIMEOUT']
        
        try:
            response = requests.post(
                url,
                json={"data": weights},
                timeout=timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            current_app.logger.error(f"Error calling standard optimizer: {str(e)}")
            return {"error": f"Error calling standard optimizer: {str(e)}"}
    
    @staticmethod
    def call_dynamic_optimizer(weights: Dict[str, float]) -> Dict[str, Any]:
        """
        Call the dynamic optimization service.
        
        Args:
            weights: Dictionary with normalized weights
            
        Returns:
            API response as dictionary
        """
        url = current_app.config['DYNAMIC_OPTIMIZER_URL']
        timeout = current_app.config['API_TIMEOUT']
        
        try:
            response = requests.post(
                url,
                json={"data": weights},  # Dynamic API expects weights in data field
                timeout=timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            current_app.logger.error(f"Error calling dynamic optimizer: {str(e)}")
            return {"error": f"Error calling dynamic optimizer: {str(e)}"}
    
    @staticmethod
    def check_api_health() -> Dict[str, bool]:
        """
        Check the health of optimization APIs.
        
        Returns:
            Dictionary with status of each API
        """
        standard_url = current_app.config['STANDARD_OPTIMIZER_URL']
        dynamic_url = current_app.config['DYNAMIC_OPTIMIZER_URL']
        timeout = 5  # Shorter timeout for health checks
        
        health = {
            "standard_optimizer": False,
            "dynamic_optimizer": False
        }
        
        # Check standard optimizer
        try:
            response = requests.get(
                standard_url.replace('/api/optimize', '/health'),
                timeout=timeout
            )
            health["standard_optimizer"] = response.status_code == 200
        except:
            pass
        
        # Check dynamic optimizer
        try:
            response = requests.get(
                dynamic_url.replace('/api/optimize', '/health'),
                timeout=timeout
            )
            health["dynamic_optimizer"] = response.status_code == 200
        except:
            pass
        
        return health
