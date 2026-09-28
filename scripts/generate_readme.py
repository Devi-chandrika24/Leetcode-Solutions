import os
import urllib.request
import json
import datetime
import re

USERNAME = 'Devi_chandrika24'
REPO_NAME = 'Leetcode-Solutions'

def get_problem_details():
    url = "https://leetcode.com/api/problems/all/"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            problems = {}
            for child in data['stat_status_pairs']:
                stat = child['stat']
                diff = child['difficulty']['level']
                title_slug = stat['question__title_slug']
                title = stat['question__title']
                q_id = stat['frontend_question_id']
                if diff == 1:
                    difficulty = '🟢 Easy'
                elif diff == 2:
                    difficulty = '🟡 Medium'
                else:
                    difficulty = '🔴 Hard'
                problems[title_slug] = {
                    'id': q_id,
                    'title': title,
                    'difficulty': difficulty,
                    'slug': title_slug
                }
            return problems
    except Exception as e:
        print(f"Error fetching problems list: {e}")
        return {}

def generate_readme():
    problems_map = get_problem_details()
    
    # Scan directories
    solutions = []
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    easy_count = 0
    medium_count = 0
    hard_count = 0
    
    # Regex to match '0001-two-sum'
    folder_pattern = re.compile(r'^(\d{4})-(.+)$')
    
    for item in sorted(os.listdir(base_dir)):
        item_path = os.path.join(base_dir, item)
        if os.path.isdir(item_path):
            match = folder_pattern.match(item)
            if match:
                q_id_padded = match.group(1)
                slug = match.group(2)
                
                # Find files inside
                files = os.listdir(item_path)
                code_file = None
                lang = "Code"
                for f in files:
                    if f.endswith('.py'):
                        code_file = f
                        lang = "Python"
                        break
                    elif f.endswith('.java'):
                        code_file = f
                        lang = "Java"
                        break
                    elif f.endswith('.cpp'):
                        code_file = f
                        lang = "C++"
                        break
                    elif f.endswith('.sql'):
                        code_file = f
                        lang = "MySQL"
                        break
                
                if code_file:
                    q_id = int(q_id_padded)
                    title = "Unknown"
                    difficulty = "Unknown"
                    
                    if slug in problems_map:
                        title = problems_map[slug]['title']
                        difficulty = problems_map[slug]['difficulty']
                    else:
                        title = " ".join([word.capitalize() for word in slug.split('-')])
                        difficulty = "🟢 Easy" # Default fallback
                        
                    if "Easy" in difficulty:
                        easy_count += 1
                    elif "Medium" in difficulty:
                        medium_count += 1
                    elif "Hard" in difficulty:
                        hard_count += 1
                        
                    # get modified date for 'Solved On'
                    statbuf = os.stat(os.path.join(item_path, code_file))
                    solved_on = datetime.datetime.fromtimestamp(statbuf.st_mtime).strftime('%Y-%m-%d')
                    
                    solutions.append({
                        'id': q_id,
                        'folder': item,
                        'title': title,
                        'slug': slug,
                        'difficulty': difficulty,
                        'lang': lang,
                        'file': code_file,
                        'solved_on': solved_on
                    })
    
    total_solved = easy_count + medium_count + hard_count
    
    readme_content = f"""# 🚀 LeetCode Solutions

> Personal collection of LeetCode solutions solved by [**DeviChandrika**](https://leetcode.com/u/{USERNAME}/) (GitHub: [@Devi-chandrika24](https://github.com/Devi-chandrika24)), committed chronologically according to solve dates.

---

### 📊 Progress Statistics

| Metric | Count |
| :--- | :--- |
| **Total Solved** | **{total_solved}** |
| 🟢 **Easy** | **{easy_count}** |
| 🟡 **Medium** | **{medium_count}** |
| 🔴 **Hard** | **{hard_count}** |

---

### 📚 Problem Solutions Index

| # | Title | Difficulty | Solution | Topic Tags | Solved On | LeetCode Link |
| :-: | :--- | :-: | :-: | :--- | :-: | :-: |
"""

    for sol in solutions:
        readme_content += f"| {sol['id']} | [{sol['title']}](./{sol['folder']}) | {sol['difficulty']} | [{sol['lang']}](./{sol['folder']}/{sol['file']}) | - | {sol['solved_on']} | [Problem](https://leetcode.com/problems/{sol['slug']}/) |\n"

    with open(os.path.join(base_dir, 'README.md'), 'w', encoding='utf-8') as f:
        f.write(readme_content)
    print("Successfully generated README.md matching requested format!")

if __name__ == "__main__":
    generate_readme()
