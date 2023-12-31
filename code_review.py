#!/usr/bin/env python3

import argparse
import os
import git
import subprocess

REQUEST = "Reply on how to improve the code for style, clarity, comments, and tests (below)\n"

def get_file(filename):
  """Get the contents of the specified file."""
  try:
    with open(filename, 'r') as file:
      file_str = file.read()
      return f"\n{filename}\n```\n{file_str}\n```"
  except FileNotFoundError:
    return f"File {filename} not found."

def get_diff(filename=None, branch='main'):
  """Get the diff between the current branch and the specified branch or from a provided file."""
  if filename:
    return get_file(filename)
  else:
    try:
      diff = subprocess.check_output(f'git diff origin/{branch}', shell=True).decode()

      if diff:
        return diff
      else:
        return "No differences between specified branch and current branch."
    except subprocess.CalledProcessError as e:
      return f"An error occurred while trying to get the git diff: {str(e)}"

def main():
  # Get arguments
  parser = argparse.ArgumentParser(description="Improve your pull requests and code base with AI-assisted code reviews")
  parser.add_argument('--persona', default='developer', help='The persona to use in the prompt (developer, kent_beck, marc_benioff, yoda)')
  parser.add_argument('--style', default='concise', help='The style of output to use (concise, zen)')
  parser.add_argument('--model', default='gpt-3.5-turbo', help='The model to use for the OpenAI API call')
  parser.add_argument('--branch', default='main', help='The branch to diff against (defaults to main)')
  parser.add_argument('--filename', default=None, help='Optional filename to use instead of git diff')
  parser.add_argument('--dir', type=str, default=None, help='Optional directory to use instead of git diff')
  
  args = parser.parse_args()

  # Switch on directory
  if args.dir:
    diff = ""
    if os.path.isdir(args.dir):
      for root, dirs, files in os.walk(args.dir):
        for file in files:
          file_path = os.path.join(root, file)
          diff += get_diff(file_path)
    else:
      print(f"The provided directory {args.dir} does not exist.")
  else:
    diff = get_diff(args.filename, args.branch)

  # Set environment variables
  os.environ["MODEL"] = args.model
  os.environ["PERSONA"] = args.persona
  os.environ["STYLE"] = args.style

  # Call action_code_review.py with the diff as input
  process = subprocess.run(["python3", "action_code_review.py"], input=diff, text=True, capture_output=True)
  print(process.stdout)

if __name__ == "__main__":
  main()
