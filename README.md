# GitHub Star Quest

[![Python Version](https://img.shields.io/badge/python-3.6%2B-blue)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green)](https://opensource.org/licenses/MIT)

Star Quest is a command-line tool that allows you to analyze the star counts of GitHub users or organizations. It fetches repository information using the GitHub API and provides insights into the total number of repositories and stars for a given user or organization.

## Features

- Retrieve repository information for a GitHub user or organization
- Sort repositories by star count in descending order
- Display the total number of repositories and stars for a user or organization
- Verbose mode to show all repositories, including those with 0 stars
- Process multiple usernames or files containing usernames
- Handle GitHub API rate limiting gracefully

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/sho-luv/star_quest.git
   ```

2. Navigate to the project directory:
   ```
   cd star_quest
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

To use the GitHub Stars Analyzer, run the following command:

```
python star_quest.py                           

             .                                                                         .   
           .o8                                                                       .o8   
 .oooo.o .o888oo  .oooo.   oooo d8b       .ooooo oo oooo  oooo   .ooooo.   .oooo.o .o888oo 
d88(  "8   888   `P  )88b  `888""8P      d88' `888  `888  `888  d88' `88b d88(  "8   888   
`"Y88b.    888    .oP"888   888          888   888   888   888  888ooo888 `"Y88b.    888   
o.  )88b   888 . d8(  888   888          888   888   888   888  888    .o o.  )88b   888 . 
8""888P'   "888" `Y888""8o d888b         `V8bod888   `V88V"V8P' `Y8bod8P' 8""888P'   "888" 
                                               888.                                        
                                               8P'                                         
                                               "                                           

usage: star_quest.py [-h] [-v] username [username ...]

Process GitHub usernames or files containing usernames and tell you how many stars they have.

positional arguments:
  username       GitHub Usernames or Orginization. Or files with usernames

options:
  -h, --help     show this help message and exit
  -v, --verbose  Show all repositories, even those with 0 stars
```

- `username`: GitHub username(s) or organization(s) to analyze. You can provide multiple usernames separated by spaces. Alternatively, you can provide file paths containing usernames, one per line.
- `-v` or `--verbose`: (Optional) Show all repositories, even those with 0 stars.
- `-h` or `--help`: Display the help message.

Examples:
```
python star_quest.py octocat
python star_quest.py google microsoft -v
python star_quest.py usernames.txt
```

## Output

The tool will display the following information for each provided username or organization:

- GitHub username or organization name
- Sorted list of repositories with their star counts
- Total number of repositories
- Total number of stars

If the provided username corresponds to an organization, the tool will additionally display the contributors for each repository.

## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

## Acknowledgements

- [GitHub API](https://docs.github.com/en/rest)
- [Requests](https://requests.readthedocs.io/)
- [Rich](https://rich.readthedocs.io/)
