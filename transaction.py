import pandas as pd
import strategy_functions as fuc

def compute_net_value_not_jump_night(data, data_open, data_low, data_high,
    direction, ai_setting, result_show):
    """compute net value list"""
    print("begin compute net value...")
    net_value = [0] * len(data)
    net_value[0] = 1
    max_value = 0
    trade_succeed = 0
    trade_times = 0
    trade_times_pro = 0
    stop_times = 0
    open_mark = 0
    close_mark = 0

    # initiate max retracement
    result_show.max_retracement = 0
    result_show.max_loss = 0.00001
    result_show.max_profit = 0.00001
    result_show.open = data_open[0]
    result_show.close = data[0]
    open = [0] * len(data)
    close = [0] * len(data)
    open_mark_counter = [0] * len(data)
    close_mark_counter = [0] * len(data)
    stop = [0] * len(data)
    for i in range(1, len(data)):
        #compute fees
        if trade_times_pro != trade_times:
            fee_mark = ai_setting.trade_fee
            trade_times_pro = trade_times
        else:
            fee_mark = 0

        # compute net value according to strategy direction
        rt = ai_setting.leverage_rate

        #transaction open
        if direction[i - 1] == 0 and direction[i] == 1 and close_mark == open_mark:
            result_show.open = data[i]
            result_show.ifstop = 0
            trade_times += 1
            open_mark += 1
            open[i] = data[i]
            open_mark_counter[i] = open_mark
        elif direction[i - 1] == 0 and direction[i] == -1 and close_mark == open_mark:
            result_show.open = data[i]
            result_show.ifstop = 0
            trade_times += 1
            open_mark += 1
            open[i] = data[i]
            open_mark_counter[i] = open_mark
        elif result_show.ifstop != 0 and direction[i] != 0 and close_mark == open_mark:
            result_show.open = data[i]
            result_show.ifstop = 0
            trade_times += 1
            open_mark += 1
            open[i] = data[i]
            open_mark_counter[i] = open_mark

        #transactioning and compute net value
        if direction[i - 1] == 1:
            if data_open[i] < result_show.open * (1 - ai_setting.stop) \
                    and open_mark > close_mark:
                net_value[i] = net_value[i - 1] * ((data_open[i] - data[i - 1])
                    * rt / data[i - 1] + 1 - fee_mark * rt)
                result_show.ifstop = 1
                stop_times += 1
                stop[i] = data_open[i]
                result_show.close = data_open[i]
                close_mark += 1
                close[i] = result_show.close
                close_mark_counter[i] = close_mark
            elif data_low[i] <= result_show.open * (1 - ai_setting.stop) \
                    and open_mark > close_mark:
                net_value[i] = net_value[i - 1] * ((result_show.open *
                    (1 - ai_setting.stop) - data[i - 1]) * rt /
                    data[i - 1] + 1 - fee_mark * rt)
                result_show.ifstop = 1
                stop_times += 1
                stop[i] = result_show.open * (1 - ai_setting.stop)
                result_show.close = result_show.open * (1 - ai_setting.stop)
                close_mark += 1
                close[i] = result_show.close
                close_mark_counter[i] = close_mark
            else:
                net_value[i] = net_value[i - 1] * ((data[i] - data[i - 1]) *
                    rt / data[i - 1] + 1 - fee_mark * rt)
            if close_mark == open_mark:
                result_show.update_max_pl_up()
        elif direction[i - 1] == -1:
            if data_open[i] > result_show.open * (1 + ai_setting.stop) \
                    and open_mark > close_mark:
                net_value[i] = net_value[i - 1] * ((data[i - 1] -
                    data_open[i]) * rt / data[i - 1] + 1 - fee_mark * rt)
                result_show.ifstop = -1
                stop_times += 1
                stop[i] = data_open[i]
                result_show.close = data_open[i]
                close_mark += 1
                close[i] = result_show.close
                close_mark_counter[i] = close_mark
            elif data_high[i] >= result_show.open * (1 + ai_setting.stop) \
                    and open_mark > close_mark:
                net_value[i] = net_value[i - 1] * ((data[i - 1] -
                result_show.open * (1 + ai_setting.stop)) *
                rt / data[i - 1] + 1 - fee_mark * rt)
                result_show.ifstop = -1
                stop_times += 1
                stop[i] = result_show.open * (1 + ai_setting.stop)
                result_show.close = result_show.open * (1 + ai_setting.stop)
                close_mark += 1
                close[i] = result_show.close
                close_mark_counter[i] = close_mark
            else:
                net_value[i] = net_value[i - 1] * ((data[i - 1] - data[i]) *
                    rt / data[i - 1] + 1 - fee_mark * rt)
            if close_mark == open_mark:
                result_show.update_max_pl_down()
        else:
            net_value[i] = net_value[i - 1]

        #transaction close
        if direction[i - 1] == 1 and direction[i] == 0 and result_show.ifstop == 0:
            if close_mark < open_mark:
                result_show.close = data[i]
                close_mark += 1
                close[i] = data[i]
                close_mark_counter[i] = close_mark
            if result_show.close > result_show.open:
                trade_succeed += 1
            if close_mark == open_mark:
                result_show.update_max_pl_up()
        elif direction[i - 1] == -1 and direction[i] == 0 and result_show.ifstop == 0:
            if close_mark < open_mark:
                result_show.close = data[i]
                close_mark += 1
                close[i] = data[i]
                close_mark_counter[i] = close_mark
            if result_show.close < result_show.open:
                trade_succeed += 1
            if close_mark == open_mark:
                result_show.update_max_pl_down()
        elif direction[i - 1] == -1 and direction[i] == 1 and result_show.ifstop == 0:
            if close_mark < open_mark:
                result_show.close = data[i]
                close_mark += 1
                close[i] = data[i]
                close_mark_counter[i] = close_mark
            if result_show.close < result_show.open:
                trade_succeed += 1
            if close_mark == open_mark:
                result_show.update_max_pl_down()
                result_show.open = data[i]
                result_show.ifstop = 0
                trade_times += 1
                open_mark += 1
                open[i] = data[i]
                open_mark_counter[i] = open_mark
        elif direction[i - 1] == 1 and direction[i] == -1 and result_show.ifstop == 0:
            if close_mark < open_mark:
                result_show.close = data[i]
                close_mark += 1
                close[i] = data[i]
                close_mark_counter[i] = close_mark
            if result_show.close > result_show.open:
                trade_succeed += 1
            if open_mark == close_mark:
                result_show.update_max_pl_up()
                result_show.open = data[i]
                result_show.ifstop = 0
                trade_times += 1
                open_mark += 1
                open[i] = data[i]
                open_mark_counter[i] = open_mark

        #update max retracement
        if net_value[i] > max_value:
            max_value = net_value[i]
        retracement = (max_value - net_value[i]) / max_value
        if retracement > result_show.max_retracement:
            result_show.max_retracement = retracement

    #update std and trade success times
    result_show.std = fuc.compute_std(net_value)
    result_show.trade_succeed = trade_succeed
    result_show.trade_times = trade_times
    result_show.stop_times = stop_times
    print("net value compute has completed.")
    out = pd.DataFrame()
    out['net_value'] = net_value
    out['open'] = open
    out['close'] = close
    out['open_mark'] = open_mark_counter
    out['close_mark'] = close_mark_counter
    out['stop'] = stop
    return out


def compute_net_value_jump_night(data, data_open, data_low, data_high,
    direction, ai_setting, result_show, data_date):
    """compute net value list"""
    print("begin compute net value...")
    net_value = [0] * len(data)
    net_value[0] = 1
    max_value = 0
    trade_succeed = 0
    trade_times = 0
    trade_times_pro = 0
    stop_times = 0
    open_mark = 0
    close_mark = 0

    # initiate max retracement
    result_show.max_retracement = 0
    result_show.max_loss = 0.00001
    result_show.max_profit = 0.00001
    result_show.open = data_open[0]
    result_show.close = data[0]
    open = [0] * len(data)
    close = [0] * len(data)
    open_mark_counter = [0] * len(data)
    close_mark_counter = [0] * len(data)
    stop = [0] * len(data)
    data_date = list(data_date)

    for i in range(1, len(data)):
        #compute fees
        if trade_times_pro != trade_times:
            fee_mark = ai_setting.trade_fee
            trade_times_pro = trade_times
        else:
            fee_mark = 0

        # compute net value according to strategy direction
        rt = ai_setting.leverage_rate


        if ai_setting.fetch_table[3:] == '1d':
            # transaction open
            if direction[i] == 1 and close_mark == open_mark:
                result_show.open = data_open[i]
                result_show.ifstop = 0
                trade_times += 1
                open_mark += 1
                open[i] = data[i]
                open_mark_counter[i] = open_mark
            if direction[i] == -1 and close_mark == open_mark:
                result_show.open = data_open[i]
                result_show.ifstop = 0
                trade_times += 1
                open_mark += 1
                open[i] = data[i]
                open_mark_counter[i] = open_mark

            #transactioning and compute net value
            if direction[i - 1] == 1:
                if data_low[i] <= result_show.open * (1 - ai_setting.stop) \
                        and open_mark > close_mark:
                    net_value[i] = net_value[i - 1] * ((result_show.open *
                        (1 - ai_setting.stop) - data_open[i]) * rt /
                        data_open[i] + 1 - fee_mark * rt)
                    result_show.ifstop = 1
                    stop_times += 1
                    stop[i] = result_show.open * (1 - ai_setting.stop)
                    result_show.close = result_show.open * (1 - ai_setting.stop)
                    close_mark += 1
                    close[i] = result_show.close
                    close_mark_counter[i] = close_mark
                else:
                    net_value[i] = net_value[i - 1] * ((data[i] - data_open[i]) *
                        rt / data_open[i] + 1 - fee_mark * rt)
                if close_mark == open_mark:
                    result_show.update_max_pl_up()
            elif direction[i - 1] == -1:
                if data_high[i] >= result_show.open * (1 + ai_setting.stop) \
                        and open_mark > close_mark:
                    net_value[i] = net_value[i - 1] * ((data_open[i] -
                    result_show.open * (1 + ai_setting.stop)) *
                    rt / data_open[i] + 1 - fee_mark * rt)
                    result_show.ifstop = -1
                    stop_times += 1
                    stop[i] = result_show.open * (1 + ai_setting.stop)
                    result_show.close = result_show.open * (1 + ai_setting.stop)
                    close_mark += 1
                    close[i] = result_show.close
                    close_mark_counter[i] = close_mark
                else:
                    net_value[i] = net_value[i - 1] * ((data_open[i] - data[i]) *
                        rt / data_open[i] + 1 - fee_mark * rt)
                if close_mark == open_mark:
                    result_show.update_max_pl_down()
            else:
                net_value[i] = net_value[i - 1]

            #transaction close
            if result_show.ifstop == 0 and close_mark < open_mark:
                if close_mark < open_mark:
                    result_show.close = data[i]
                    close_mark += 1
                    close[i] = data[i]
                    close_mark_counter[i] = close_mark
                if result_show.close > result_show.open:
                    trade_succeed += 1

        elif ai_setting.fetch_table[3:] != '1d':
            #transaction open
            if direction[i - 1] == 0 and direction[i] == 1 \
                    and close_mark == open_mark and data_date[i][11:] \
                    != '15:00:00' and data_date[i][11:] != '15:05:00' \
                    and data_date[i][11:] != '15:10:00' and \
                    data_date[i][11:] != '15:15:00':
                result_show.open = data[i]
                result_show.ifstop = 0
                trade_times += 1
                open_mark += 1
                open[i] = data[i]
                open_mark_counter[i] = open_mark
            elif direction[i - 1] == 0 and direction[i] == -1 \
                    and close_mark == open_mark:
                result_show.open = data[i]
                result_show.ifstop = 0
                trade_times += 1
                open_mark += 1
                open[i] = data[i]
                open_mark_counter[i] = open_mark
            elif result_show.ifstop != 0 and direction[i] != 0 \
                    and close_mark == open_mark:
                result_show.open = data[i]
                result_show.ifstop = 0
                trade_times += 1
                open_mark += 1
                open[i] = data[i]
                open_mark_counter[i] = open_mark

            # transactioning and compute net value
            if direction[i - 1] == 1:
                if data_open[i] < result_show.open * (1 - ai_setting.stop) \
                        and open_mark > close_mark:
                    net_value[i] = net_value[i - 1] * ((data_open[i] - data[i - 1])
                                * rt / data[i - 1] + 1 - fee_mark * rt)
                    result_show.ifstop = 1
                    stop_times += 1
                    stop[i] = data_open[i]
                    result_show.close = data_open[i]
                    close_mark += 1
                    close[i] = result_show.close
                    close_mark_counter[i] = close_mark
                elif data_low[i] <= result_show.open * (1 - ai_setting.stop) \
                        and open_mark > close_mark:
                    net_value[i] = net_value[i - 1] * ((result_show.open *
                            (1 - ai_setting.stop) - data[i - 1]) * rt /
                            data[i - 1] + 1 - fee_mark * rt)
                    result_show.ifstop = 1
                    stop_times += 1
                    stop[i] = result_show.open * (1 - ai_setting.stop)
                    result_show.close = result_show.open * (
                                1 - ai_setting.stop)
                    close_mark += 1
                    close[i] = result_show.close
                    close_mark_counter[i] = close_mark
                else:
                    net_value[i] = net_value[i - 1] * (
                                (data[i] - data[i - 1]) *
                                rt / data[i - 1] + 1 - fee_mark * rt)
                if close_mark == open_mark:
                    result_show.update_max_pl_up()
            elif direction[i - 1] == -1:
                if data_open[i] > result_show.open * (1 + ai_setting.stop) \
                        and open_mark > close_mark:
                    net_value[i] = net_value[i - 1] * ((data[i - 1] -
                        data_open[i]) * rt / data[i - 1] + 1 - fee_mark * rt)
                    result_show.ifstop = -1
                    stop_times += 1
                    stop[i] = data_open[i]
                    result_show.close = data_open[i]
                    close_mark += 1
                    close[i] = result_show.close
                    close_mark_counter[i] = close_mark
                elif data_high[i] >= result_show.open * (
                        1 + ai_setting.stop) \
                        and open_mark > close_mark:
                    net_value[i] = net_value[i - 1] * ((data[i - 1] -
                        result_show.open * (1 + ai_setting.stop)) *
                        rt / data[i - 1] + 1 - fee_mark * rt)
                    result_show.ifstop = -1
                    stop_times += 1
                    stop[i] = result_show.open * (1 + ai_setting.stop)
                    result_show.close = result_show.open * (1 + ai_setting.stop)
                    close_mark += 1
                    close[i] = result_show.close
                    close_mark_counter[i] = close_mark
                else:
                    net_value[i] = net_value[i - 1] * (
                                (data[i - 1] - data[i]) *
                                rt / data[i - 1] + 1 - fee_mark * rt)
                if close_mark == open_mark:
                    result_show.update_max_pl_down()
            else:
                net_value[i] = net_value[i - 1]

            #transaction close
            if direction[i - 1] == 1 and direction[i] == 0 \
                    and result_show.ifstop == 0:
                if close_mark < open_mark:
                    result_show.close = data[i]
                    close_mark += 1
                    close[i] = data[i]
                    close_mark_counter[i] = close_mark
                if result_show.close > result_show.open:
                    trade_succeed += 1
                if close_mark == open_mark:
                    result_show.update_max_pl_up()
            elif direction[i - 1] == -1 and direction[i] == 0 \
                    and result_show.ifstop == 0:
                if close_mark < open_mark:
                    result_show.close = data[i]
                    close_mark += 1
                    close[i] = data[i]
                    close_mark_counter[i] = close_mark
                if result_show.close < result_show.open:
                    trade_succeed += 1
                if close_mark == open_mark:
                    result_show.update_max_pl_down()
            elif direction[i - 1] == -1 and direction[i] == 1 \
                    and result_show.ifstop == 0:
                if close_mark < open_mark:
                    result_show.close = data[i]
                    close_mark += 1
                    close[i] = data[i]
                    close_mark_counter[i] = close_mark
                if result_show.close < result_show.open:
                    trade_succeed += 1
                if close_mark == open_mark:
                    result_show.update_max_pl_down()
                    result_show.open = data[i]
                    result_show.ifstop = 0
                    trade_times += 1
                    open_mark += 1
                    open[i] = data[i]
                    open_mark_counter[i] = open_mark
            elif direction[i - 1] == 1 and direction[i] == -1 \
                    and result_show.ifstop == 0:
                if close_mark < open_mark:
                    result_show.close = data[i]
                    close_mark += 1
                    close[i] = data[i]
                    close_mark_counter[i] = close_mark
                if result_show.close > result_show.open:
                    trade_succeed += 1
                if open_mark == close_mark:
                    result_show.update_max_pl_up()
                    result_show.open = data[i]
                    result_show.ifstop = 0
                    trade_times += 1
                    open_mark += 1
                    open[i] = data[i]
                    open_mark_counter[i] = open_mark
            elif data_date[i][11:] == '15:00:00':
                if close_mark < open_mark:
                    result_show.close = data[i]
                    close_mark += 1
                    close[i] = data[i]
                    close_mark_counter[i] = close_mark
                if result_show.close > result_show.open:
                    trade_succeed += 1

        #update max retracement
        if net_value[i] > max_value:
            max_value = net_value[i]
        retracement = (max_value - net_value[i]) / max_value
        if retracement > result_show.max_retracement:
            result_show.max_retracement = retracement

    #update std and trade success times
    result_show.std = fuc.compute_std(net_value)
    result_show.trade_succeed = trade_succeed
    result_show.trade_times = trade_times
    result_show.stop_times = stop_times
    print("net value compute has completed.")
    out = pd.DataFrame()
    out['net_value'] = net_value
    out['open'] = open
    out['close'] = close
    out['open_mark'] = open_mark_counter
    out['close_mark'] = close_mark_counter
    out['stop'] = stop
    return out