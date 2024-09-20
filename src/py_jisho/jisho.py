import json
import requests
import traceback

BASE_URL: str = 'https://jisho.org/api/v1/search/words?keyword='


def _parse_data(payload: dict) -> dict:
    """Parses given payload and returns a formatted dictionary.

    Args:
        payload (dict): Payload from Jisho API to parse.

    Returns:
        dict: Resulting formatted dictionary to return
    """
    result: dict = {}

    for entry in payload.get('data', {}):
        slug = entry.get('slug', '')
        senses = entry.get('senses', [])
        reading = entry.get('japanese', {})[0].get('reading', '')

        result[slug] = {
            'reading': reading,
            'definition': ', '.join(senses[0].get('english_definitions', [])),
            'parts_of_speech': ', '.join(senses[0].get('parts_of_speech', []))
        }
    
    return result


def search(keyword: str) -> dict:
    """Searches Jisho API finding any matches to input query.

    Args:
        keyword (str): Keyword to search by. Keyword can be in the form of romaji or english. (i.e. "ki" will search for words containing romaji ki).

    Returns:
        dict: Dictionary containing matches containing meaning and part of speech.
    """

    url = BASE_URL + keyword

    try:
        r = requests.get(url, verify=False)
        r_json = r.json()

        result: dict = _parse_data(r_json)
        print(result)

    except Exception as err:
        print(f'[ERROR] Error occurred when querying API:\n{traceback.format_exc(err)}')


if __name__ == '__main__':
    search('ki')