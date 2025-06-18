"""
Utilidades para el procesamiento de texto y extracción de parámetros.
"""
import re
import random
import json
from typing import Dict, Optional, Tuple, List
from rapidfuzz import process, fuzz
from nltk.corpus import stopwords
import nltk
from flask import current_app

# Asegurar que los stopwords estén descargados
try:
    nltk.download('stopwords', quiet=True)
except Exception as e:
    print(f"Error downloading stopwords: {str(e)}")

def clean_param_phrase(phrase: str) -> str:
    """
    Cleans a parameter phrase, preserving important keywords.
    """
    # List of keywords that should NOT be removed
    important_keywords = {
        'public', 'transport', 'congestion', 'emissions', 'operational', 'cost',
        'traffic', 'delay', 'frequency'
    }
    
    try:
        stop_words = set(stopwords.words('english')) | {
            'optimize', 'adjust', 'set', 'want', 'priority', 'dynamic', 'standard'
        }
        
        words = phrase.split()
        cleaned_words = [
            word for word in words 
            if (word.lower() not in stop_words or word.lower() in important_keywords) 
            and len(word) > 2
        ]
        return " ".join(cleaned_words).strip()
    except Exception as e:
        print(f"Error in clean_param_phrase: {str(e)}")
        return phrase.strip()

def sample_priority(priority: str, priority_intervals: Dict[str, Tuple[float, float]]) -> float:
    """
    Generates a value within the specified priority interval.
    Uses the midpoint of the interval for greater consistency and predictability.
    """
    try:
        interval = priority_intervals.get(priority.lower())
        if not interval:
            raise ValueError(f"Unknown priority: {priority}")
        
        # Use the midpoint of the interval instead of a random value
        return round((interval[0] + interval[1]) / 2, 2)
    except Exception as e:
        print(f"Error in sample_priority: {str(e)}")
        return 0.1

def find_parameter_improved(param_phrase: str, param_map: Dict[str, str], cutoff: int = 70) -> Optional[str]:
    """
    Finds the API parameter that best matches the given phrase.
    Uses fuzzy matching with an adjusted threshold.
    """
    try:
        normalized_input = param_phrase.strip().lower()
        if normalized_input in param_map:
            return param_map[normalized_input]
        choices = list(param_map.keys())
        best_match = process.extractOne(normalized_input, choices, scorer=fuzz.ratio)
        if best_match and best_match[1] >= cutoff:
            return param_map[best_match[0]]
        return None
    except Exception as e:
        print(f"Error in find_parameter_improved: {str(e)}")
        return None

def interpret_user_input(user_input: str, default_weights: Dict[str, float], 
                        priority_intervals: Dict[str, Tuple[float, float]]) -> Tuple[Dict[str, float], str]:
    """
    Interprets user input to extract weights and determine optimizer type.
    Enhanced version that ensures correct interpretation of priorities.
    """
    weights = default_weights.copy()
    user_input_lower = user_input.lower()
    optimizer_type = "standard_optimizer"

    # More robust detection of dynamic optimization
    dynamic_keywords = ["dynamic", "real-time", "adaptive", "real time"]
    if any(keyword in user_input_lower for keyword in dynamic_keywords):
        optimizer_type = "dynamic_optimizer"
        # We don't remove keywords from text to avoid interpretation issues
    
    param_map = {
        "public transport": "weight_PublicTransport",
        "congestion": "weight_Congestion",
        "emissions": "weight_Emissions",
        "operational cost": "weight_OperationalCost"
    }

    # Pattern A modified: more flexible with what follows after priority
    pattern_a = re.compile(
        r"(very high|high|medium|low|very low)\s+priority\s+(?:to|for)\s+([a-z\s]+?)(?=(?:,|and|\s+for|\s+to|$))",
        re.IGNORECASE
    )
    
    # Pattern B modified: more flexible with what follows after priority
    pattern_b = re.compile(
        r"([a-z\s]+?)\s+(very high|high|medium|low|very low)\s+priority(?=(?:,|and|\s+for|\s+to|$|\s+optimization))",
        re.IGNORECASE
    )

    for match in pattern_a.finditer(user_input_lower):
        priority_word = match.group(1)
        param_phrase = clean_param_phrase(match.group(2).strip())
        api_param = find_parameter_improved(param_phrase, param_map)
        if api_param:
            weights[api_param] = sample_priority(priority_word, priority_intervals)

    for match in pattern_b.finditer(user_input_lower):
        param_phrase = clean_param_phrase(match.group(1).strip())
        priority_word = match.group(2)
        api_param = find_parameter_improved(param_phrase, param_map)
        if api_param:
            weights[api_param] = sample_priority(priority_word, priority_intervals)

    pattern_numeric = re.compile(
        r"([a-z\s]+?)\s+(?:to|=|:)\s+(\d+(?:\.\d+)?)",
        re.IGNORECASE
    )
    for match in pattern_numeric.finditer(user_input_lower):
        param_phrase = clean_param_phrase(match.group(1).strip())
        numeric_value = float(match.group(2))
        api_param = find_parameter_improved(param_phrase, param_map)
        if api_param:
            weights[api_param] = numeric_value

    # Add logging for debugging
    print(f"DEBUG - Interpreted weights: {weights}")
    print(f"DEBUG - Optimizer type: {optimizer_type}")
    
    return weights, optimizer_type

def validate_weight(weight: float, param_name: str) -> Tuple[float, str]:
    """
    Validates that a weight is within the allowed range (0-1).
    Returns the validated weight and a warning message if adjustment was necessary.
    """
    warning = ""
    
    # Validate limits
    if weight < 0:
        warning = f"Warning: Weight for {param_name} ({weight}) was negative. Adjusted to 0."
        weight = 0
    elif weight > 1:
        warning = f"Warning: Weight for {param_name} ({weight}) exceeded 1. Adjusted to 1."
        weight = 1
    
    return weight, warning

def validate_weights(weights: Dict[str, float]) -> Tuple[Dict[str, float], List[str]]:
    """
    Validates all weights in the dictionary.
    Returns the validated weights and a list of warnings.
    """
    validated = {}
    warnings = []
    
    for param, value in weights.items():
        valid_value, warning = validate_weight(value, param)
        validated[param] = valid_value
        if warning:
            warnings.append(warning)
    
    return validated, warnings

def normalize_weights(weights: Dict[str, float]) -> Dict[str, float]:
    """
    Normalizes weights to sum to 1.0.
    """
    total = sum(weights.values())
    if total <= 0:
        return weights  # Cannot normalize if sum is zero or negative
    
    return {k: round(v / total, 2) for k, v in weights.items()}

def extract_and_format_results(api_response: dict, optimizer_type: str) -> str:
    """
    Extracts and formats API results for presentation to the user.
    """
    try:
        if optimizer_type == "standard_optimizer":
            # Format standard optimizer results
            kpis = api_response.get("KPIs", {})
            diffs = kpis.get("difference", {})
            
            if not diffs:
                return "No differences found in standard optimizer response."
            
            lines = ["🚦 Standard Traffic Optimizer Results:"]
            
            # Always show the payload if available
            if "debug_payload" in api_response:
                payload = api_response.get("debug_payload", {})
                lines.append("\nWeights used in optimization:")
                for param, value in payload.items():
                    # Convert technical name to friendly name
                    friendly_name = param.replace("weight_", "").replace("PublicTransport", "Public Transport").replace("OperationalCost", "Operational Cost")
                    lines.append(f"- {friendly_name}: {value}")
                lines.append("")  # blank line
            
            for metric, value in diffs.items():
                percentage = abs(round(value * 100, 2))
                if value > 0:
                    lines.append(f"The KPI '{metric}' improves by {percentage}%.")
                elif value < 0:
                    lines.append(f"The KPI '{metric}' worsens by {percentage}%.")
                else:
                    lines.append(f"The KPI '{metric}' shows no change.")
            
            return "\n".join(lines)
        
        elif optimizer_type == "dynamic_optimizer":
            # Format dynamic optimizer results
            # Assume data is in the "data" key or at the root
            results_data = api_response.get("data", api_response)
            
            expected_kpis = ["Income", "Congestion inside", "Congestion (Delay)", "Emissions"]
            lines = ["🚦 Dynamic Traffic Optimizer Results:"]
            
            # Always show the payload if available
            if "debug_payload" in api_response:
                payload = api_response.get("debug_payload", {})
                lines.append("\nWeights used in optimization:")
                for param, value in payload.items():
                    # Convert technical name to friendly name
                    friendly_name = param.replace("weight_", "").replace("PublicTransport", "Public Transport").replace("OperationalCost", "Operational Cost")
                    lines.append(f"- {friendly_name}: {value}")
                lines.append("")  # blank line
            
            found_kpis = False
            for kpi in expected_kpis:
                if kpi in results_data:
                    value = results_data[kpi]
                    lines.append(f"The value for '{kpi}' is {value}.")
                    found_kpis = True
            
            if not found_kpis:
                return "No dynamic optimizer results found or results are not in the expected format."
            
            return "\n".join(lines)
        
        else:
            return f"Unknown optimizer type: {optimizer_type}"
            
    except Exception as e:
        return f"Error processing API response results: {str(e)}"
