# How to contribute

I'm really glad you're reading this, because we need volunteer developers to help this project come to fruition.

Here are some important resources:

  * [Our Documentation](https://pytenable.rtfd.io) is a good resource as to what is currently considered stable.
  * [Our roadmap](https://github.com/tenable/pyTenable/milestones) is a 10k ft. view of where we're headed.
  * [The Tenable Community Integrations Section](https://community.tenable.com/s/topic/0TOf2000000HPDKGA4) is a great place to discuss working with the Tenable APIs in general.
  * Bugs? [Github Issues](https://github.com/tenable/pyTenable/issues) is where to report them

## Testing

We use py.test extensively to test inputs, outputs, and failure conditions.  Further we use tooling to record the interactions with the APIs (VCRpy) when we would be making a successful call so that there is a consistency to whats being tested against.

## Submitting changes

Please send a [GitHub Pull Request to pyTenable](https://github.com/tenable/pyTenable/pull/new/master) with a clear list of what you've done (read more about [pull requests](http://help.github.com/pull-requests/)). When you send a pull request, we will love you forever if you include unit tests, documentation, and code comments.  We can always use more test coverage. Please follow our coding conventions (below) and make sure all of your commits are atomic (one feature per commit).

Always write a clear log message for your commits. One-line messages are fine for small changes, but bigger changes should look like this:

    $ git commit -m "A brief summary of the commit
    > 
    > A paragraph describing what changed and its impact."

## Coding conventions

Start reading our code and you'll get the hang of it. We optimize for readability:

  * We indent using four spaces (soft tabs)
  * We use Google Doc-strings format
  * We conform to PEP8 as much as possible, only breaking convention when necessary.
  * We ALWAYS put spaces after list items and method parameters (`[1, 2, 3]`, not `[1,2,3]`), around operators (`x += 1`, not `x+=1`).
  * This is open source software. Consider the people who will read your code, and make it look nice for them. It's sort of like driving a car: Perhaps you love doing donuts when you're alone, but with passengers the goal is to make the ride as smooth as possible.
    * Code Readability is paramount.  If something is difficult to follow, we generally expect the code to be broken down into readable & manageable components.
    * Code should be commented not only to describe what it is, but should also help to tell the story of what we are tryign to accomplish and why.
    * We generally prefer to conform to DRY as often as possible, however will break DRY for purpose of readability.
  * We prefer that all classes are in camelCase.
  * We generally want all function names and variables to be in snake_case.  There are notable exceptions to this (especially in Tenable.sc) when it's simply unavoidable.
  * The documentation is directly generated from the source code, this means that well-formed doc-strings are critical.

Thanks,
Steven McGrath, Tenable, Inc.
