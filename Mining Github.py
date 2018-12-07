#17-1. Other Languages: Modify the API call in python_repos.py so it generates a chart showing the most popular projects
#in other languages . Try languages such as JavaScript, Ruby, C, Java, Perl, Haskell, and Go .

import requests
import pygal
from pygal.style import LightColorizedStyle as LCS, LightenStyle as LS

url = 'https://api.github.com/search/repositories?q=language:c&sort=stars'
r = requests.get(url)
print("Status code:", r.status_code)

response_dict = r.json()
print("Total repositories:", response_dict['total_count'])

repo_dicts = response_dict['items']

names, plot_dicts = [], []
for repo_dict in repo_dicts:
    names.append(repo_dict['name'])

    description = repo_dict['description']
    if not description:
        description = "No description provided."

    plot_dict = {
        'value': repo_dict['stargazers_count'],
        'label': description,
        'xlink': repo_dict['html_url'],
        }
    plot_dicts.append(plot_dict)

my_style = LS('#333366', base_style=LCS)
my_style.title_font_size = 24
my_style.label_font_size = 14
my_style.major_label_font_size = 18

my_config = pygal.Config()
my_config.x_label_rotation = 45
my_config.show_legend = False
my_config.truncate_label = 15
my_config.show_y_guides = False
my_config.width = 1000

chart = pygal.Bar(my_config, style=my_style)
chart.title = 'Most-Starred Python Projects on GitHub'
chart.x_labels = names

chart.add('', plot_dicts)
chart.render_to_file('python_repos.svg')

#17-2. Active Discussions: Using the data from hn_submissions.py, make a bar chart showing the most active discussions
#currently happening on Hacker News . The height of each bar should correspond to the number of comments each submission
#has . The label for each bar should include the submission’s title, and each bar should act as a link to the discussion
#page for that submission .

import requests
import pygal
from pygal.style import LightColorizedStyle as LCS, LightenStyle as LS

from operator import itemgetter

url = 'https://hacker-news.firebaseio.com/v0/topstories.json'
r = requests.get(url)
print("Status code:", r.status_code)

submission_ids = r.json()
submission_dicts = []
for submission_id in submission_ids[:30]:
    url = ('https://hacker-news.firebaseio.com/v0/item/' +
           str(submission_id) + '.json')
    submission_r = requests.get(url)
    print(submission_r.status_code)
    response_dict = submission_r.json()

    submission_dict = {
        'title': response_dict['title'],
        'link': 'http://news.ycombinator.com/item?id=' + str(submission_id),
        'comments': response_dict.get('descendants', 0)
    }
    submission_dicts.append(submission_dict)

submission_dicts = sorted(submission_dicts, key=itemgetter('comments'),
                          reverse=True)

for submission_dict in submission_dicts:
    print("\nTitle:", submission_dict['title'])
    print("Discussion link:", submission_dict['link'])
    print("Comments:", submission_dict['comments'])

titles, plot_dicts = [], []
for submission_dict in submission_dicts:
    titles.append(submission_dict['title'])
    plot_dict = {
        'value': submission_dict['comments'],
        'label': submission_dict['title'],
        'xlink': submission_dict['link'],
    }
    plot_dicts.append(plot_dict)

my_style = LS('#333366', base_style=LCS)
my_style.title_font_size = 24
my_style.label_font_size = 14
my_style.major_label_font_size = 18

my_config = pygal.Config()
my_config.x_label_rotation = 45
my_config.show_legend = False
my_config.truncate_label = 15
my_config.show_y_guides = False
my_config.width = 1000
my_config.y_title = 'Number of Comments'

chart = pygal.Bar(my_config, style=my_style)
chart.title = 'Most Active Discussions on Hacker News'
chart.x_labels = titles

chart.add('', plot_dicts)
chart.render_to_file('hn_discussions.svg')

#17-3. Testing python_repos.py: In python_repos.py, we printed the value of status_code to make sure the API call was
#successful . Write a program called test_python_repos.py, which uses unittest to assert that the value of status_code
#is 200 . Figure out some other assertions you can make—for example, that the number of items returned is expected and
#that the total number of repositories is greater than a certain amount .

import requests
import pygal
from pygal.style import LightColorizedStyle as LCS, LightenStyle as LS

def get_response():
    url = 'https://api.github.com/search/repositories?q=language:python&sort=stars'
    r = requests.get(url)
    return r

def get_repo_dicts(response):
    response_dict = r.json()
    repo_dicts = response_dict['items']
    return repo_dicts

def get_names_plot_dicts(repo_dicts):
    names, plot_dicts = [], []
    for repo_dict in repo_dicts:
        names.append(repo_dict['name'])

        description = repo_dict['description']
        if not description:
            description = "No description provided."

        plot_dict = {
            'value': repo_dict['stargazers_count'],
            'label': description,
            'xlink': repo_dict['html_url'],
            }
        plot_dicts.append(plot_dict)
    return names, plot_dicts

def make_visualization(names, plot_dicts):
    my_style = LS('#333366', base_style=LCS)
    my_style.title_font_size = 24
    my_style.label_font_size = 14
    my_style.major_label_font_size = 18

    my_config = pygal.Config()
    my_config.x_label_rotation = 45
    my_config.show_legend = False
    my_config.truncate_label = 15
    my_config.show_y_guides = False
    my_config.width = 1000

    chart = pygal.Bar(my_config, style=my_style)
    chart.title = 'Most-Starred Python Projects on GitHub'
    chart.x_labels = names

    chart.add('', plot_dicts)
    chart.render_to_file('python_repos.svg')


r = get_response()
repo_dicts = get_repo_dicts(r)
names, plot_dicts = get_names_plot_dicts(repo_dicts)
make_visualization(names, plot_dicts)