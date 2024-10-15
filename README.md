# Plot Helper

A very simple function for creating subplots using list-like structures.

## Motivation

While doing some research projects, I need to create dozens of plots
for a single dataset, the axes of which need to be configurable between Chinese
and English. Moreover, I need to add additional plots or subplots from
time to time. The original plot-generating style of `matplotlib` becomes very
annoying at this point. I don't want my plots to be "so customizable", but I
do want them to be consistent and precise. It would be better if I can define
my plots in some list- or dict-like structure, which to me would be easier
to be managed.

## Requirements

In general, `python >= 3.8` with `matplotlib` installed
should be fine. You will probably need `pandas` to manage your data.

To run the `plot_helper_example.ipynb` you'll need `jupyter notebook`.

## Usage

See `plot_helper_example.ipynb` for more detail. Some notes here:

1. Only one left axis is allowed for a single subplot (multiple right axes
   might be defined).
1. **New from 10/15/2024** you may now manually specify other keyword
   arguments for title, xlabel, ylabel and legend. See
   `plot_helper_example.ipynb` for more detail.
1. ...

As mentioned in previous parts, this script does not care that much about
the flexibility and customization but focuses on consistency.

## Misc

You can freely use this code. I don't expect this to be helpful to everyone.
I probably don't have enough time and effort to maintain the code and answer
the questions as well.

## History

### 2024/10/15

1. Update `plot_helper.py`: one may now manually specify other keyword
   arguments for title, xlabel, ylabel and legend.
2. Update the `plot_helper_example.ipynb` script accordingly.

### 2024/03/12

1. Replace `add_subplot` function with `matplotlib.pyplot.subplots` to create
   all subplots at once.
2. Use `getattr` function to support more types of plots.
3. Use `**kwargs` to support passing all supported keyword arguments of
   `matplotlib.pyplot.subplots`.
4. Add support to generating multi-column subplot figures.
5. Update the `plot_helper_example.ipynb` script accordingly.
