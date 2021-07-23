# Contributing to MKE Budet

## Reporting Issues

*Issue tickets* can be used to track feature requests, report bugs, ask questions,
or just pose general comments. The issue ticketing system can be accessed with
a (free) GitHub account at [this page](https://github.com/milwaukee-city-data/budget/issues).

When opening an issue to report a problem, please try to provide a minimal code
example that reproduces the issue along with details of the operating
system and the Python version you are using.

## Contributing Code

**Imposter syndrome disclaimer**: We want your help and you are welcome here.

Most of us, especially early in our adult lives, have an inner monologue telling
us that we're not ready to contribute to major ongoing projects. That our
skills aren't nearly good enough to meaningfully help, or that we wouldn't even
know where to start. "What could I *possibly* offer a project like this one?"

We want to assure you that while this feeling is natural, it could not be further
from the truth. If you're curious about the community you live in, if you ever
wonder where or how the City spends its money or cares for its people, you are
ready to contribute and we are eager to have you. It is not only a fantastic way
to advance your own critical thinking and coding skills, but also a pragmatic way
to participate in your community democratically, on small scales and large. We
keep us safe which means we keep us informed.

Moreover, **writing perfect code is never the measure of a good analyst.** It's
imperative to try to create things, make mistakes, then learn from those mistakes
and from openly sharing with others. That's how we all improve, and as a community
we are happy to help others learn.

Contributing to this project also doesn't just mean writing code. You can help out
enormously by writing documentation, checking our work, or giving feedback about
the project, which very much includes feedback about the contribution process.
This kind of input may even be the most valuable to the project in the long
term, because you can more easily spot the errors and assumptions that longtime
contributors have glossed over. A steady stream of fresh eyes works to keep
communication freely flowing.

**Note:** This disclaimer is based on one written by
[Adrienne Lowe](https://github.com/adriennefriend) for a
[PyCon talk](https://www.youtube.com/watch?v=6Uj746j9Heo), and was adapted for
this project based on its use in the [Astropy](https://github.com/astropy/astropy/)
and [GWpy](https://github.com/gwpy/gwpy/) contributing guides.

## Development model (for coders)

This repository uses the [GitHub flow](https://guides.github.com/introduction/flow/)
collaborative development model.

In short, contributions to this repository are made via pull requests from GitHub
users' forks of the main [MKE budget repository](https://github.com/milwaukee-city-data/budget).
The basic idea is to use the `main` branch of your fork as a way of keeping
your fork up-to-date with other contributors' changes that have been merged
into the main repo, then adding/changing new features on a dedicated *feature
branch* for each development project.

If this is your first contribution, make sure you have a GitHub account
(signing up is free of charge) and set up a development sandbox as follows:

*   Create the fork (if needed) by clicking *Fork* in the upper-right corner of
    <https://github.com/milwaukee-city-data/budget/>. (This only needs to be done once,
    ever.)

*   From the command-line, if you haven't already, clone your fork (replace
    `<username>` with your GitHub username):

    ```bash
    git clone https://github.com/<username>/budget.git mke-budget-fork
    cd mke-budget-fork
    ```

*   Link your cloned fork to the upstream "main" repo:

    ```bash
    git remote add upstream https://github.com/milwaukee-city-data/budget.git
    ```

For each development project:

*   Pull changes from the upstream "main" repo onto your fork's `main` branch
    to pick up other people's changes, then push to your remote to update your
    fork on github.com

    ```bash
    git pull --rebase upstream main
    git push
    ```

*   Create a new branch for this project with a short, descriptive name

    ```bash
    git checkout -b my-project
    ```

*   Make commits to this branch

*   Push changes to your remote on github.com

    ```bash
    git push -u origin my-project
    ```

*   Open a *merge request* (also known as a *pull request*) on github.com and
    tag the lead developer (@alurban) to initiate an interactive code review

*   When the request is merged, you should "delete the source branch" (there's a
    button) to keep your fork clean, and delete it from your local clone:

    ```bash
    git checkout main
    git branch -D my-project
    git pull upstream main
    ```

That's all there is to it!

**Note:** merge requests should be as simple as possible to keep the repository
clean, so if you have multiple contributions in mind, they should be split up
over multiple merge requests.
