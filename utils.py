def jaccard_similarity(str1, str2):
    """
    Calculate the Jaccard similarity coefficient between two strings.
    The Jaccard similarity is defined as the size of the intersection divided by 
    the size of the union of the sample sets.
    
    Args:
        str1, str2: Strings to compare
        
    Returns:
        float: Jaccard similarity coefficient between 0.0 and 1.0
    """
    # Convert strings to sets of words
    set1 = set(str1.lower().split())
    set2 = set(str2.lower().split())
    
    # Calculate intersection and union
    intersection = set1.intersection(set2)
    union = set1.union(set2)
    
    # Return Jaccard similarity coefficient
    if len(union) == 0:
        return 0.0
    return len(intersection) / len(union)


def levenshtein_distance(s1, s2):
    """
    Calculate the Levenshtein (edit) distance between two strings.
    
    Args:
        s1, s2: Strings to compare
        
    Returns:
        int: The edit distance between the strings
    """
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)

    if len(s2) == 0:
        return len(s1)

    previous_row = list(range(len(s2) + 1))
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    
    return previous_row[-1]


def word_similarity(s1, s2):
    """
    Calculate similarity between two words using both Jaccard and edit distance.
    
    Args:
        s1, s2: Words to compare
        
    Returns:
        float: Similarity score between 0.0 and 1.0
    """
    jaccard_sim = jaccard_similarity(s1, s2)
    
    # Calculate normalized edit distance similarity
    max_len = max(len(s1), len(s2))
    if max_len == 0:
        return 1.0  # Both empty strings are identical
    
    edit_distance = levenshtein_distance(s1.lower(), s2.lower())
    edit_sim = 1.0 - (edit_distance / max_len)
    
    # Combine both measures (average)
    combined_sim = (jaccard_sim + edit_sim) / 2.0
    return combined_sim


def find_most_similar_keyword(text, keywords, threshold=0.6):
    """
    Find the most similar keyword in the text based on combined similarity measures.
    This implementation handles variations in spelling by using both Jaccard similarity
    and edit distance.
    
    Args:
        text (str): The text to search in
        keywords (list): List of keywords to look for
        threshold (float): Minimum similarity threshold (0.0 to 1.0)
        
    Returns:
        tuple: (keyword, similarity_score, start_index, end_index) or (None, 0, -1, -1) if not found
    """
    text_lower = text.lower()
    best_match = (None, 0, -1, -1)  # (keyword, similarity, start_idx, end_idx)
    
    for keyword in keywords:
        keyword_lower = keyword.lower()
        keyword_words = keyword_lower.split()
        
        # First, try to find exact keyword matches using sliding window
        words = text_lower.split()
        keyword_len = len(keyword_words)
        
        # Slide through the text to find potential matches of same length
        for i in range(len(words) - keyword_len + 1):
            # Form a substring of the same length as the keyword
            substr_words = words[i:i + keyword_len]
            substr = ' '.join(substr_words)
            
            # Calculate combined similarity
            similarity = jaccard_similarity(substr, keyword_lower)
            
            # Update best match if similarity is above threshold and better than current best
            if similarity >= threshold and similarity > best_match[1]:
                # Calculate the character positions in the original text
                temp_words = text.split()
                start_char = 0
                for j in range(i):
                    start_char += len(temp_words[j]) + 1  # +1 for the space
                
                end_char = start_char
                for j in range(i, i + keyword_len):
                    end_char += len(temp_words[j]) + 1  # +1 for the space (except for the last word)
                
                end_char -= 1  # Remove the last space
                
                best_match = (keyword, similarity, start_char, end_char)
        
        # Second, try a character-based sliding window for more flexible matching
        # This helps catch misspellings and variations
        for i in range(len(text_lower)):
            for j in range(i + 1, min(len(text_lower) + 1, i + len(keyword_lower) + 5)):  # Allow a few extra chars
                substr = text_lower[i:j]
                
                # Calculate similarity between this substring and the keyword
                similarity = jaccard_similarity(substr, keyword_lower)
                
                # Also try the word similarity for better misspelling detection
                if similarity < threshold:
                    similarity = word_similarity(substr, keyword_lower)
                
                if similarity >= threshold and similarity > best_match[1]:
                    best_match = (keyword, similarity, i, j)
    
    return best_match