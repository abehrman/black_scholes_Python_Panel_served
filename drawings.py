import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from black_scholes_merton import BSMoption

#def draw_both_tables(vars, baseCall, basePut):
def draw_both_tables(vars, baseCall):
    # spot, exercise, sigma, time, rate, dividend_rate

    myOpt = BSMoption(*vars)
    mrmgCall = myOpt.black_scholes_call()
    #mrmgPut = myOpt.black_scholes_put()

    draw_input_table(vars)
    #draw_output_table(baseCall, basePut, mrmgCall, mrmgPut)
    draw_output_table(baseCall, mrmgCall)


def draw_input_table(vars):
    # modified from https://towardsdatascience.com/simple-little-tables-with-matplotlib-9780ef5d0bc4

    title_text = 'Input Values'
    footer_text = 'Jan 22, 2021'
    fig_background_color = 'skyblue'
    fig_border = 'steelblue'

    plt.figure(linewidth=2,
            edgecolor=fig_border,
            facecolor=fig_background_color,
            tight_layout={'pad':1},
            figsize=(4,3.5)
            )

    rowNames = 'spot, exercise, sigma, time, rate, dividend_rate'.split(', ')
    colNames = ['values']

    rcolors = plt.cm.BuPu(np.full(len(rowNames), 0.1))
    ccolors = plt.cm.BuPu(np.full(len(colNames), 0.1))

    the_table = plt.table(cellText = [[str(var)] for i, var in enumerate(vars)],
                        cellLoc = 'left',
                        rowLabels=rowNames,
                        rowColours=rcolors,
                        rowLoc='right',
                        colColours=ccolors,
                        colLabels=colNames,
                        loc='center')

    #plt.table(cellText = [[rowNames[i], str(var)] for i, var in enumerate(vars)])
    # Scaling is the only influence we have over top and bottom cell padding.
    # Make the rows taller (i.e., make cell y scale larger).
    the_table.scale(1, 2)
    # Hide axes
    ax = plt.gca()
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    # Hide axes border
    plt.box(on=None)
    # Add title
    plt.suptitle(title_text, size=16)
    # Add footer
    plt.figtext(0.95, 0.05, footer_text, horizontalalignment='right', size=8, weight='light')
    # Force the figure to update, so backends center objects correctly within the figure.
    # Without plt.draw() here, the title will center on the axes and not the figure.
    plt.show()
    # Create image. plt.savefig ignores figure edge and face colors, so map them.

#def draw_output_table(baseCall, basePut, mrmgCall, mrmgPut):
def draw_output_table(baseCall, mrmgCall):
    base_call_px = baseCall
    #base_put_px = basePut

    mrmg_call_px = mrmgCall
    #mrmg_put_px = mrmgPut

    call_diff = (mrmg_call_px / base_call_px) - 1
    #put_diff = (mrmg_put_px / base_put_px) - 1

    # modified from https://towardsdatascience.com/simple-little-tables-with-matplotlib-9780ef5d0bc4

    cell_text = [
        [str(round(base_call_px,5)), str(round(mrmg_call_px,5))],
        ['',f'{round(call_diff * 100,2)}%'],
        #[str(round(base_put_px,5)), str(round(mrmg_put_px,5))],
        #['',f'{round(put_diff * 100,2)}%']
    ]

    title_text = 'Call and Put Prices'
    footer_text = 'Jan 22, 2021'
    fig_background_color = 'skyblue'
    fig_border = 'steelblue'

    plt.figure(linewidth=2,
            edgecolor=fig_border,
            facecolor=fig_background_color,
            tight_layout={'pad':1},
            figsize=(4,3.5)
            )

    #rowNames = 'Call, Call Diff (%), Put, Put Diff (%)'.split(', ')
    rowNames = 'Call, Call Diff (%)'.split(', ')
    colNames = 'Value, MRMG Value'.split(', ')

    rcolors = plt.cm.BuPu(np.full(len(rowNames), 0.1))
    ccolors = plt.cm.BuPu(np.full(len(colNames), 0.1))

    the_table = plt.table(cellText = cell_text,
                        cellLoc = 'center',
                        rowLabels=rowNames,
                        rowColours=rcolors,
                        rowLoc='right',
                        colColours=ccolors,
                        colLabels=colNames,
                        loc='center')

    #plt.table(cellText = [[rowNames[i], str(var)] for i, var in enumerate(vars)])
    # Scaling is the only influence we have over top and bottom cell padding.
    # Make the rows taller (i.e., make cell y scale larger).
    the_table.scale(1, 2)
    # Hide axes
    ax = plt.gca()
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    # Hide axes border
    plt.box(on=None)
    # Add title
    plt.suptitle(title_text, size=16)
    # Add footer
    plt.figtext(0.95, 0.05, footer_text, horizontalalignment='right', size=8, weight='light')
    # Force the figure to update, so backends center objects correctly within the figure.
    # Without plt.draw() here, the title will center on the axes and not the figure.
    plt.draw()
    # Create image. plt.savefig ignores figure edge and face colors, so map them.

def sensitivity_table(myOpt, var, sensitivity_label, sensitivity_vals, AON_FVs):
    sensitivity_label = sensitivity_label
    sensitivity_vals = sensitivity_vals
    AON_FVs = AON_FVs

    call_pxs = []
    for val in sensitivity_vals:
        call_pxs.append(round(myOpt.black_scholes_call(**{var:val}),2))

    df = pd.DataFrame(zip(sensitivity_vals, AON_FVs, call_pxs), columns=[sensitivity_label,'AON Value','MRMG Value'])
    df['Value Diff'] = np.round(df['AON Value'] - df['MRMG Value'],2)
    df['Value Diff'].apply(lambda x: f'{x:0.2f}')
    df['Percent Diff'] = ((df['MRMG Value'] / df['AON Value']) - 1)
    df['Percent Diff'] = df['Percent Diff'].apply(lambda x: f'{float(x) * 100:0.2f}%')

    #df = df.set_index(sensitivity_label,drop=True)

    cell_text = df.values

    title_text = f'Senitivity - {sensitivity_label}' 
    footer_text = 'Jan 22, 2021'
    fig_background_color = 'skyblue'
    fig_border = 'steelblue'

    plt.figure(linewidth=2,
            edgecolor=fig_border,
            facecolor=fig_background_color,
            tight_layout={'pad':1},
            figsize=(8,7)
            )

    #rowNames = 'Call, Call Diff (%), Put, Put Diff (%)'.split(', ')
    rowNames = df.index.values
    colNames = df.columns

    rcolors = plt.cm.BuPu(np.full(len(rowNames), 0.1))
    ccolors = plt.cm.BuPu(np.full(len(colNames), 0.1))

    the_table = plt.table(cellText = cell_text,
                        cellLoc = 'center',
                        #rowLabels=rowNames,
                        #rowColours=rcolors,
                        #rowLoc='right',
                        colColours=ccolors,
                        colLabels=colNames,
                        loc='center')

    #plt.table(cellText = [[rowNames[i], str(var)] for i, var in enumerate(vars)])
    # Scaling is the only influence we have over top and bottom cell padding.
    # Make the rows taller (i.e., make cell y scale larger).
    the_table.scale(1, 2)
    # Hide axes
    ax = plt.gca()
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    # Hide axes border
    plt.box(on=None)
    # Add title
    plt.suptitle(title_text, size=16)
    # Add footer
    plt.figtext(0.95, 0.05, footer_text, horizontalalignment='right', size=8, weight='light')
    # Force the figure to update, so backends center objects correctly within the figure.
    # Without plt.draw() here, the title will center on the axes and not the figure.
    #plt.draw()
    # Create image. plt.savefig ignores figure edge and face colors, so map them.

    return plt