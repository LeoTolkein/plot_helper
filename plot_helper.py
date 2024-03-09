
# * Plot helper
# * Using list-like structure to customize vertical subplots
# * This module relies on matplotlib


from typing import Tuple
import matplotlib.pyplot as plt

def single_plotter(plot_settings_list: list,
                figsizewidth: float = 8.0,
                figsizeheight: float = 2.0, 
                dpi: int = 300,
            ) -> Tuple[plt.Figure, list]:
    """ Generate a single figure and return the figure and a list containing
        the main axes of it. This function will call 
        `matplotlib.pyplot.figure` and `figure.add_subplot` functions to 
        create subplots. 
        
        Inputs: 
        `plot_settings_list`: a list containing multiple dicts, with each dict
        defining a subplot. Each subplot will have the same width and height
        defined by the input `figsizewidth` and `figsizeheight`. 

        `figsizewidth`: width of the figure. Default is 8.

        `figsizeheight`: height of each subplot. Default is 2. Note that when
        there is only one subplot for the figure, the figsizeheight will be
        doubled to make the figure more square-like.

        `dpi`: the DPI of figure.

        Outputs:
        `fig`: the matplotlib.pyplot.Figure object generated.

        `axes_x_list`: a list containing all axes that defines the x-axis of
        each subplot (i.e. the main axis) will be returned so that one can 
        easily make modifications to the x-axis. Note that the additional axes
        for each subplot will not be contained.

    """

    plotnum = len(plot_settings_list)
    assert plotnum > 0, "No information for plotting!"
    # * Create figure with constrained (similar to tight) layout
    if plotnum == 1:
        fig = plt.figure(dpi=dpi, figsize=(figsizewidth, 2 * figsizeheight), layout="constrained")
    else:
        fig = plt.figure(dpi=dpi, figsize=(figsizewidth, figsizeheight * plotnum), layout="constrained")
    axes_x_list = []
    # * Create and plot each subplot
    # * main axis for each subplot will also be saved for further use
    for idx in range(plotnum):
        ax_idx = fig.add_subplot(int(f"{plotnum}1{idx+1}"))
        single_subplot_dict = plot_settings_list[idx]
        left_yaxisplot_dict = single_subplot_dict["yaxes"][0]
        if len(single_subplot_dict["yaxes"]) == 1:
            _axes_plot_helper(ax_idx, left_yaxisplot_dict)
        else:
            _axes_plot_helper(ax_idx, left_yaxisplot_dict, plot_legend=False)
            all_lines_list, all_labels_list = ax_idx.get_legend_handles_labels()
            # * When multiple axes exist for one subplot, the first axis will
            # * be regarded as the major axis (left y axis), and the rests will
            # * be the minor axis (right y axes). Will generate only one single
            # * legend for each subplot, and only the legend setting for the 
            # * major axis will work; the settings for minor axes will be ignored.
            right_y_pos = 1
            for right_yaxisplot_dict in single_subplot_dict["yaxes"][1:]:
                ax_right = ax_idx.twinx()
                ax_right.spines["right"].set_position(("axes", right_y_pos))
                _axes_plot_helper(ax_right, right_yaxisplot_dict, plot_legend=False)
                lines_right, labels_right = ax_right.get_legend_handles_labels()
                all_lines_list = all_lines_list + lines_right
                all_labels_list = all_labels_list + labels_right
                right_y_pos += 0.2
            if left_yaxisplot_dict.get("legend") is not None:
                # * NOTE that although the settings for the left y axis is used,
                # * the legend is actually attached to the last right y axis, 
                # * just to avoid overlapping of legend information
                if left_yaxisplot_dict["legend"]["visible"] == True:
                    ax_right.legend(
                        all_lines_list,
                        all_labels_list,
                        loc=left_yaxisplot_dict["legend"]["loc"]
                    )
            else:
                ax_right.legend(all_lines_list, all_labels_list)
        if single_subplot_dict.get("xlim") is not None:
            if isinstance(single_subplot_dict["xlim"], dict):
                # * set lim as bottom and top format
                ax_idx.set_xlim(**single_subplot_dict["xlim"])
            else:
                # * set lim as array-like format
                ax_idx.set_xlim(single_subplot_dict["xlim"])
        if single_subplot_dict.get("xlabel") is not None:
            ax_idx.set_xlabel(single_subplot_dict["xlabel"])
        if single_subplot_dict.get("title") is not None:
            ax_idx.set_title(single_subplot_dict["title"])
        axes_x_list.append(ax_idx)
    # * return figure itself and axes list
    return fig, axes_x_list


def _axes_plot_helper(some_ax: plt.Axes, some_ax_dict: dict, 
            plot_legend: bool = True) -> None:
    """ Plot helper for a single axis
    """

    for lineplot_dict in some_ax_dict["lines"]:
        x_data = lineplot_dict.get("x", None)
        specs = lineplot_dict.get("spec", None)
        if lineplot_dict["type"] == "curve":
            plot_func = some_ax.plot
        elif lineplot_dict["type"] == "scatter":
            plot_func = some_ax.scatter

        if x_data is None:
            if specs is None:
                plot_func(lineplot_dict["y"])
            else:
                plot_func(lineplot_dict["y"], **specs)
        else:
            if specs is None:
                plot_func(x_data, lineplot_dict["y"])
            else:
                plot_func(x_data, lineplot_dict["y"], **specs)
    if some_ax_dict.get("ylabel") is not None:
        some_ax.set_ylabel(some_ax_dict["ylabel"])
    if some_ax_dict.get("ylim") is not None:
        if isinstance(some_ax_dict["ylim"], dict):
            some_ax.set_ylim(**some_ax_dict["ylim"])
        else:
            some_ax.set_ylim(some_ax_dict["ylim"])
    if some_ax_dict.get("grid") is not None:
        some_ax.grid(**some_ax_dict["grid"])
    if plot_legend:
        if some_ax_dict.get("legend") is not None:
            if some_ax_dict["legend"]["visible"] == True:
                some_ax.legend(loc=some_ax_dict["legend"]["loc"])
        else:
            some_ax.legend()
