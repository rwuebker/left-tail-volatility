"""Part 1 figures; reusable calculations live in the tested modules."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def plot_shock_responses(table, previous_variance, path):
    fig, axes = plt.subplots(1, 2, figsize=(10, 4.5), sharey=True)
    for ax, model in zip(axes, ['GARCH-t', 'GJR-GARCH-t']):
        part = table.loc[table.model == model]
        for sign, label, color in [(1, 'Positive shock', '#167c80'), (-1, 'Negative shock', '#c44e52')]:
            values = part.loc[part.shock_percent * sign > 0].copy()
            values['magnitude'] = values.shock_percent.abs()
            values = values.sort_values('magnitude')
            ax.plot(values.magnitude, values.next_daily_volatility_percent, marker='o',
                    color=color, linestyle='-' if sign == 1 else '--', label=label, linewidth=2)
        ax.set(title=model, xlabel='Absolute shock (% return)', xticks=[1, 2, 4])
        ax.spines[['top', 'right']].set_visible(False)
        ax.grid(axis='y', alpha=.2)
        ax.legend(frameon=False)
    axes[0].set_ylabel('Next-day conditional volatility (%)')
    fig.suptitle('Does the sign of a shock change the response?', fontsize=14)
    fig.text(.5, .01, f'Same prior variance in both models: {previous_variance:.3f} percent². Shocks are deviations from the fitted mean.', ha='center', fontsize=8)
    fig.tight_layout(rect=(0, .05, 1, .94))
    fig.savefig(path, dpi=220, bbox_inches='tight')
    plt.close(fig)


def plot_training_volatility(train, fits, path):
    fig, axes = plt.subplots(2, 1, figsize=(11, 6), sharex=True)
    axes[0].plot(train.index, train * 100, color='#526575', linewidth=.5)
    axes[0].set_ylabel('Daily return (%)')
    for name in ['GARCH-t', 'GJR-GARCH-t']:
        axes[1].plot(train.index, fits[name].conditional_volatility, label=name, linewidth=.8)
    axes[1].set_ylabel('Daily volatility (%)')
    axes[1].legend(frameon=False)
    for ax in axes:
        ax.spines[['top', 'right']].set_visible(False)
        ax.grid(axis='y', alpha=.2)
    fig.suptitle('Training sample: returns and fitted conditional volatility')
    fig.text(.5, .01, 'In-sample fitted paths use parameters estimated from the whole training sample; they are not historical out-of-sample forecasts.', ha='center', fontsize=8)
    fig.tight_layout(rect=(0, .04, 1, .96))
    fig.savefig(path, dpi=220, bbox_inches='tight')
    plt.close(fig)
