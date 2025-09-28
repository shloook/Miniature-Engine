import re
from spellchecker import SpellChecker

# language_tool_python is optional (requires Java at runtime). We attempt to import it;
# if it's unavailable or initialization fails we fall back to lightweight heuristics.
try:
    import language_tool_python
except Exception:
    language_tool_python = None

spell = SpellChecker()

# Initialize language tool if possible
tool = None
if language_tool_python is not None:
    try:
        tool = language_tool_python.LanguageTool('en-US')
    except Exception:
        tool = None

def match_case(original: str, suggestion: str) -> str:
    """Adjust suggestion's casing to match the original word's casing."""
    if original.isupper():
        return suggestion.upper()
    if original.istitle():
        return suggestion.capitalize()
    if original and original[0].isupper():
        return suggestion.capitalize()
    return suggestion

def tokenize_words(text: str):
    """Return list of (word, start, end) for words including apostrophes/hyphens."""
    pattern = re.compile(r"[A-Za-z0-9]+(?:['-][A-Za-z0-9]+)?")
    return [(m.group(0), m.start(), m.end()) for m in pattern.finditer(text)]

def check_spelling_and_structure(text: str) -> dict:
    # Tokenize
    tokens = tokenize_words(text)
    words_lower = [t[0].lower() for t in tokens]

    # Spell check
    misspelled = set(spell.unknown(words_lower))
    misspellings = []
    for (token, start, end), lower in zip(tokens, words_lower):
        if lower in misspelled:
            suggestions = list(spell.candidates(lower))
            try:
                best = spell.correction(lower)
                if best and best not in suggestions:
                    suggestions.insert(0, best)
            except Exception:
                pass
            # Apply original case to suggestions
            suggestions_cased = [match_case(token, s) for s in suggestions]
            misspellings.append({
                'word': token,
                'start': start,
                'end': end,
                'suggestions': suggestions_cased
            })

    # Build corrected text by replacing misspelled words with the top suggestion (if any)
    corrected_text = text
    for m in sorted(misspellings, key=lambda x: x['start'], reverse=True):
        if m['suggestions']:
            corrected_text = corrected_text[:m['start']] + m['suggestions'][0] + corrected_text[m['end']:]

    # Structure suggestions
    structure_suggestions = []
    if tool is not None:
        try:
            matches = tool.check(text)
            for match in matches:
                structure_suggestions.append({
                    'message': match.message,
                    'offset': match.offset,
                    'length': match.errorLength,
                    'replacements': match.replacements[:5]
                })
        except Exception:
            # If LanguageTool fails at runtime, ignore and fall back
            tool_local = None
    else:
        # Lightweight heuristics if LanguageTool isn't available
        sentences = re.split(r'(?<=[.!?])\\s+', text)
        for s in sentences:
            if len(s) > 120:
                structure_suggestions.append({
                    'message': 'Long sentence detected (over 120 characters). Consider splitting it.',
                    'example': s[:200]
                })
            if re.search(r"\\bvery\\s+\\w+", s, flags=re.I):
                structure_suggestions.append({
                    'message': "Avoid using weak intensifiers like 'very' — prefer a stronger adjective.",
                    'example': s
                })
            # crude passive voice detection (may produce false positives)
            if re.search(r"\\b(is|was|were|be|been|being|are|am)\\b\\s+\\w+ed\\b", s, flags=re.I):
                structure_suggestions.append({
                    'message': 'Possible passive voice detected. Consider using active voice.',
                    'example': s
                })

    return {
        'original': text,
        'words': misspellings,
        'corrected_text': corrected_text,
        'structure_suggestions': structure_suggestions
    }
