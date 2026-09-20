from typing import List, Dict, Any

def find_label_by_name(labels: List[Dict[str, Any]], name: str) -> List[Dict[str, Any]]:
    """Ищет лейблы по названию."""
    results = []
    for label in labels:
        if name.lower() in label['name'].lower():
            results.append(label)
    return results