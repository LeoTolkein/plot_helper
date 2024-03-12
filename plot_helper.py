
# * Plot helper
# * Using list-like structure to customize vertical subplots
# * This module relies on matplotlib


from typing import Tuple, Union
import numpy as np
import matplotlib.pyplot as plt

def single_plotter(plot_settings_list: Union[list, np.ndarray],
                figsizewidth: float = 4.0,
                figsizeheight: float = 2.0, 
                right_yaxis_interval: float = 0.2, 
                dpi: int = 300,
                layout: str = "constrained",
                **kwargs,
            ) -> Tuple[plt.Figure, np.ndarray]:
    """ Generate a single figure and return the figure and a list containing
        the main axes of it. This function will call 
        `matplotlib.pyplot.figure` and `figure.add_subplot` functions to 
        create subplots. 

        NOTE: if you wants to create plots containing non-Roman characters
        (e.g. Chinese, Japanese, and Korean), you need to set the matplotlib
        prior to the use of this function. This function will NOT automatically
        set the matplotlib according to your language.
        
        Inputs: 
        `plot_settings_list`: 1D or 2D Array-like. If it is 1D, it will be
        iternally transformed into a 2D array with shape (-1, 1) (a vertical
        2D array). Each element in this 2D array is a dict defining a
        subplot. Each subplot will have the same width and height defined
        by figsizewidth and figsizeheight. 

        Note that if you want to leave some subplots blank (e.g., you have a 
        3x3 subplot arrangement but you want to leave the subplot on the 
        position axes[2, 2] blank), then use an empty dict {} or None to
        occupy that position.

        `figsizewidth`: width of the figure. Default is 4. Note that when
        there is only one column of subplots for the figure, the figsizeheight 
        will be doubled.

        `figsizeheight`: height of each subplot. Default is 2. Note that when
        there is only one row of subplots for the figure, the figsizeheight 
        will be doubled.

        `right_yaxis_interval`: how far does each y axis lie from its neighbors.
        By default it is 0.2.

        `dpi`: Same as the matplotlib.pyplot.plot keyword `dpi`. By
        default it is set as 300 to make clear figures.

        `layout`: Same as the matplotlib.pyplot.plot keyword `layout`. By
        default it is set as "constrained" to make elegant figures. 

        You may use other keyword arguments supported by `matplotlib.pyplot.plot`
        function, but do NOTE that `figsize` should not be passed
        as the figsize of the whole figure will be determined by the size
        of `plot_settings_list`, `figsizeweight`, and `figsizeheight`.

        Outputs:
        `fig`: the matplotlib.pyplot.Figure object generated.

        `axes`: a 2D np.ndarray containing all axes that defines the
        x-axis of each subplot (i.e. the main axes) will be returned so that
        one can easily make modifications to the x-axis. This array is
        essentially the one created by the `matplotlib.pyplot.subplots`
        function. NOTE that different from `ax` returned by `subplots`, 
        if there is only one subplot (i.e. ncol=nrow=1), axes will be a
        1D array containing 1 axis element, instead of merely an `Axes` object.
        This is for the convenience of iteration.
        Also note that the additional axes for each subplot will not be
        contained.
    """
    plotsarr = np.array(plot_settings_list, dtype=object)
    plotnum = plotsarr.size
    assert plotnum > 0, "No information for plotting!"
    assert len(plotsarr.shape) <= 2, "Too many dimensions for plot setting list!"

    # * If plotsarr is 1D, transform it into a 2D array.
    # * otherwise the shape of plotsarr is maintained
    if len(plotsarr.shape) == 1: 
        plotsarr = plotsarr.reshape(-1, 1)
    # * Double the height and width if any of them is 1.
    if plotsarr.shape[0] == 1: figsizeheight = 2 * figsizeheight
    if plotsarr.shape[1] == 1: figsizewidth = 2 * figsizewidth

    # * Create figure with constrained (similar to tight) layout
    fig, axes = plt.subplots(
        nrows=plotsarr.shape[0], ncols=plotsarr.shape[1],
        figsize=(figsizewidth * plotsarr.shape[1], 
                figsizeheight * plotsarr.shape[0]), 
        dpi=dpi,
        layout=layout,
        **kwargs,
    )

    if plotsarr.shape[0] == 1 and plotsarr.shape[1] == 1:
        axes = np.array([axes], dtype=object)

    # * Plot on each subplot axis
    for idx in range(plotnum):
        # * By numpy official doc, iteration is done in row-major, 
        # * C-style order
        ax_main = axes.flat[idx]
        single_subplot_dict = plotsarr.flat[idx]
        _subplot_helper(
                        ax_main=ax_main, 
                        single_subplot_dict=single_subplot_dict,
                        right_yaxis_interval=right_yaxis_interval,
                    )

    # * return figure itself and axes list
    return fig, axes


def _subplot_helper(
                    ax_main: plt.Axes, 
                    single_subplot_dict: Union[dict, None], 
                    right_yaxis_interval: float = 0.2, 
                ) -> None:
    if not single_subplot_dict:
        # * if single_subplot_dict is None or {}, then just hide this
        # * subplot. 
        ax_main.axis("off")
    else:
        yaxes = single_subplot_dict.get("yaxes", None)
        left_yaxisplot_dict = yaxes[0]
        if len(yaxes) == 1:
            _axes_plot_helper(ax_main, left_yaxisplot_dict)
        else:
            # * When multiple axes exist for one subplot, the first axis will
            # * be regarded as the major axis (left y axis), and the rests will
            # * be the minor axis (right y axes). Will generate only one single
            # * legend for each subplot, and only the legend setting for the 
            # * major axis will work; the settings for minor axes will be 
            # * ignored.
            _axes_plot_helper(ax_main, left_yaxisplot_dict, plot_legend=False)
            all_lines_list, all_labels_list = ax_main.get_legend_handles_labels()
            right_y_pos = 1
            for right_yaxisplot_dict in yaxes[1:]:
                ax_right = ax_main.twinx()
                ax_right.spines["right"].set_position(("axes", right_y_pos))
                _axes_plot_helper(ax_right, right_yaxisplot_dict, plot_legend=False)
                lines_right, labels_right = ax_right.get_legend_handles_labels()
                all_lines_list = all_lines_list + lines_right
                all_labels_list = all_labels_list + labels_right
                right_y_pos += right_yaxis_interval
            legend_settings = left_yaxisplot_dict.get("legend", None)
            if legend_settings is not None:
                # * NOTE that although the settings for the left y axis is used,
                # * the legend is actually attached to the last right y axis, 
                # * just to avoid overlapping of legend information
                if legend_settings["visible"] == True:
                    ax_right.legend(
                        all_lines_list,
                        all_labels_list,
                        loc=legend_settings["loc"]
                    )
            else:
                ax_right.legend(all_lines_list, all_labels_list)
        xlim_settings = single_subplot_dict.get("xlim", None)
        if xlim_settings is not None:
            # * set lim as bottom and top format
            if isinstance(xlim_settings, dict): ax_main.set_xlim(**xlim_settings)
            # * set lim as array-like format
            else: ax_main.set_xlim(xlim_settings)
        xlabel_settings = single_subplot_dict.get("xlabel", None)
        if xlabel_settings is not None: ax_main.set_xlabel(xlabel_settings)
        title_settings = single_subplot_dict.get("title", None)
        if title_settings is not None: ax_main.set_title(title_settings)


def _axes_plot_helper(some_ax: plt.Axes, some_ax_dict: dict, 
            plot_legend: bool = True) -> None:
    """ Plot helper for a single axis
    """

    for lineplot_dict in some_ax_dict["lines"]:
        x_data = lineplot_dict.get("x", None)
        specs = lineplot_dict.get("spec", None)
        if lineplot_dict["type"] == "curve":
            plot_func = some_ax.plot
        else:
            plot_func = getattr(some_ax, lineplot_dict["type"])

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
    ylabel_settings = some_ax_dict.get("ylabel", None)
    if ylabel_settings is not None: some_ax.set_ylabel(ylabel_settings)

    ylim_settings = some_ax_dict.get("ylim", None)
    if ylim_settings is not None:
        # * set lim as bottom and top format
        if isinstance(ylim_settings, dict): some_ax.set_ylim(**ylim_settings)
        # * set lim as array-like format
        else: some_ax.set_ylim(ylim_settings)
    grid_settings = some_ax_dict.get("grid", None)
    if grid_settings is not None: some_ax.grid(**grid_settings)
    if plot_legend:
        legend_settings = some_ax_dict.get("legend", None)
        if legend_settings is not None:
            if legend_settings["visible"] == True:
                some_ax.legend(loc=legend_settings["loc"])
        else: some_ax.legend()
