import os
import numpy as np
import xlrd
import matplotlib.pyplot as plt
from graph import FindLargestBandwith

COLOR_MAP = plt.cm.rainbow #nipy_spectral, Set1,Paired  sequential: 'viridis' cubehelix, jet, rainbow, RdBu, tab20b

########################################################
'''task_executed 是已经完成的任务【名称：【完成的时间点（不是运行时间），在数据中心‘id’上运行和保存数据， 所属job】】
task_current是正在进行的任务
因为数据中心不是相互连接的，所以会有一些job和任务无法进行（我假设两个不直接相连的数据中心无法通信）
如果假设可以数据中心可以中转，才能计算出所有任务，需要你用图算法算一下所有数据中心之间的两两带宽

task_executed = {} ## name: [finish time, datacenterID, job, start+time]

新的BANDWITH = FindLargestBandwith(BANDWITH)
'''

BANDWITH = [[1000, 80, 150, 0, 0, 0, 0, 0, 0, 0, 0, 500, 0],
            [80, 1000, 122, 250, 175, 0, 0, 0, 0, 0, 0, 0, 0],
            [100, 104, 1000, 210, 45, 0, 0, 300, 0, 0, 400, 0, 0],
            [0, 200, 205, 1000, 20, 160, 0, 0, 300, 0, 0, 0, 0],
            [0, 169, 36, 15, 1000, 200, 190, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 160, 210, 1000, 0, 90, 0, 0, 53, 0, 500],
            [0, 0, 0, 0, 205, 0, 1000, 0, 0, 66, 37, 0, 0],
            [0, 0, 300, 0, 0, 78, 0, 1000, 0, 0, 66, 37, 0, 0],
            [0, 0, 0, 300, 0, 0, 0, 26, 1000, 0, 93, 500, 0],
            [0, 0, 0, 0, 0, 0, 54, 50, 0, 1000, 0, 0, 0],
            [0, 0, 400, 0, 0, 42, 64, 0, 67, 0, 1000, 0, 0],
            [500, 0, 0, 0, 0, 0, 0, 0, 500, 0, 0, 1000, 500],
            [0, 0, 0, 0, 0, 500, 0, 0, 0, 0, 0, 500, 1000]] # MBps

#BANDWITH = FindLargestBandwith(BANDWITH)

TOTAL_SLOTS = [2, 1, 3, 2, 1, 4, 2, 1, 2, 1, 1, 4, 4]

DATA_PARTITION = {'A1': 0, 'B1': 0, 'C1': 1, 'B2': 2, 'A2':3, 'E1':3, 'D1':4, 'C2':5, 'E2':5, 'D2':6, 'E3':7, 'D3': 8, 'F1': 8, 'F3': 9, 'E4':10, 'F4': 11, 'F5':12, 'F2':12}

EXE_NAME = 'exe_time'

TOTOAL_DATACENTER = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]

JOB = ['A', 'B', 'C', 'D', 'E', 'F']
# JOB = ['A', 'B', 'C', 'E', 'F']

TASK_TOTAL = {'A':['tA1', 'tA2'], 'B':['tB1', 'tB2'], 'C':['tC1', 'tC2', 'tC3'], 'D':['tD1', 'tD2', 'tD3', 'tD4', 'tD5'], 'E':['tE1', 'tE2', 'tE3', 'tE4', 'tE5', 'tE6'], 'F':['tF1', 'tF2', 'tF3', 'tF4', 'tF5', 'tF6', 'tF7', 'tF8', 'tF9']
}

JOBS_PRIORITY = {'A': {1:['tA1', 'tA2']}, 'B': {1: ['tB1'], 2:['tB2']}, 'C': {1: ['tC1'], 2: ['tC2'], 3:['tC3']}, 'D': {1: ['tD1', 'tD2'], 2: ['tD3', 'tD4'], 3:['tD5']}, 'E': {1:['tE1'], 2: ['tE2', 'tE3'], 3:['tE4', 'tE5'], 4:['tE6']}, 'F':{1:['tF1'], 2:['tF2', 'tF3', 'tF4'], 3:['tF5', 'tF6'], 4:['tF7', 'tF8'], 5:['tF9']}
}


def Compute_task_min_completion_time(task_information, available_slot_state, t, task_executed, bandwith):
    min_completion_time_value = 65535
    min_completion_time_task2DC = []
    ####compute the minimum compeltion time
    data_source = task_information[t].keys()
    for locate_in in range(len(TOTOAL_DATACENTER)): ## locate_in-> data center
        if available_slot_state[locate_in] != 0:
            compl = 0
            for data in data_source: ## calculate completion time
                if data == EXE_NAME:
                    compl += task_information[t][data]
                elif data in task_executed:
                    data_resouce_center = task_executed[data][1]
                    bw = bandwith[data_resouce_center][locate_in]
                    if bw == 0:
                        compl = 655350
                    else:
                        compl += task_information[t][data]/bw
                else:
                    data_resouce_center = DATA_PARTITION[data]
                    bw = bandwith[data_resouce_center][locate_in]
                    if bw == 0:
                        compl = 655350
                    else:
                        compl += task_information[t][data]/bw
            if compl <=  min_completion_time_value:
                min_completion_time_value = compl
                min_completion_time_task2DC = locate_in
    return min_completion_time_value, min_completion_time_task2DC

def main():
    print('hello world')
    # a = TASK_TOTAL
    Final_BW = FindLargestBandwith(BANDWITH)
    data = xlrd.open_workbook('ToyData.xlsx')
    table = data.sheet_by_name(u'Job List')
    task_information = {}
    for row in range(1, 28):
        task_name = table.cell(row, 1).value
        task_information[task_name] = {}
        for col in range(2,38):
            if table.cell(row, col).value != '':
                data_source = table.cell(0, col).value
                task_information[task_name][data_source] = table.cell(row, col).value
        task_information[task_name][EXE_NAME] = table.cell(row, 38).value

    task_executed = {} ## name: [finish time, datacenterID, job, start+time]
    task_current = {} ## name: [remaining time, datacenterID, job, complection_time]
    time_stamp = 0
    jobs_current_task = {} 
    for jb in JOB:
        jobs_current_task[jb] = 0
    available_slot_state = {} ## the number of available slots on each datacenter
    for dc in range(13): ## initialize slot
        available_slot_state[dc] = TOTAL_SLOTS[dc]
    slot_free = True
    task_free = True
    Onload = True
    available_datacenter = TOTOAL_DATACENTER

    while Onload:
        while slot_free and task_free:
            lauch_job = [] 
            # min_tasks_num = 65535
            # for job in JOB:
            #     if jobs_current_task[job] <= min_tasks_num:
            #         min_tasks_num = jobs_current_task[job]
            min_tasks_num = min(jobs_current_task.values())
            for job in JOB:
                if jobs_current_task[job] == min_tasks_num:
                    remain_task = False
                    for task in TASK_TOTAL[job]:
                        if task not in task_executed:
                            remain_task = True ### if all tasks of the job have been finished, remain_task = False
                    if remain_task:
                        lauch_job.append(job)
            ##### planning for lauch one task of job ########
            task_condidate = {}
            for job in lauch_job:
                # task_free = False
                for stage in range(len(JOBS_PRIORITY[job])): # search available task to execute
                    tasks = JOBS_PRIORITY[job][stage+1]
                    for t in tasks:
                        if t not in task_executed and t not in task_current:
                            if stage == 0:
                                # task_condidate.append(t)
                                current_task_minc, current_task_min_loc = Compute_task_min_completion_time(task_information, available_slot_state, t, task_executed, Final_BW)
                                if current_task_minc <= 1000:
                                    task_condidate[t] = [current_task_minc, current_task_min_loc, job] ## lable the time and slot
                            else:
                                data_source = task_information[t].keys()
                                parents_finish = True
                                for s in data_source:
                                    if s in TASK_TOTAL[job] and s not in task_executed:
                                        parents_finish = False
                                if parents_finish:
                                    current_task_minc, current_task_min_loc = Compute_task_min_completion_time(task_information, available_slot_state, t, task_executed, Final_BW)
                                    if current_task_minc <= 1000:
                                        task_condidate[t] = [current_task_minc, current_task_min_loc, job] ## lable the time and slot
                                # del data_source[-1]
            ######### 1-select a task that has minimum completion time from task condidate, push it to task_current, 
            # 2-then remove one slot in available_slot_state
            # 3-check whether there are slots available, if not, set slot_free = False
            # 4- check whether there are tasks in task condidate, if not set task_free = False
            ##########
            ##########  step 1
            if task_condidate == {}:
                task_free = False
                if task_current == {}:
                    Onload = False
            else:
                min_compl = 65535
                for task in task_condidate:
                    if task_condidate[task][0] <= min_compl:
                        min_compl = task_condidate[task][0]
                        select_task = task
                #execte !!!       
                jobs_current_task[task_condidate[select_task][2]] += 1 ### execte a task of this job
                datacenter_loc = task_condidate[select_task][1]
                of_job = task_condidate[select_task][2]
                task_current[select_task] = [min_compl, datacenter_loc, of_job, task_condidate[select_task][0]]
                assert available_slot_state[datacenter_loc] != 0
                available_slot_state[datacenter_loc] -= 1
                if max(available_slot_state.values()) == 0:
                    slot_free = False
                if len(task_condidate) == 1:
                    task_free = False
        
        if Onload == False:
            break
        fig = plt.figure()
        ax1 = fig.add_subplot(311)

        data_x = []
        data_y = []
        # SCHEMES_REW = []
        for job in JOB:
            for task in task_current:
                if task_current[task][2] == job:
                    data_x.append(task + ':DC' + str(task_current[task][1]))
                    data_y.append([task_current[task][0], task_current[task][3]])
                    # SCHEMES_REW.append(task + ':' + 'DC' + str(task_current[task][1]))
        # ax1.plot(data_x, data_y)
        colors = [COLOR_MAP(i) for i in np.linspace(0, 1, len(data_x))]
        pos = 0.5
        index = 0
        x_label_pos = []
        for task in data_x:
            plt.bar(pos, data_y[index][0], alpha =0.8, width = 0.3, color = colors[index], edgecolor = 'k')
            plt.bar(pos, data_y[index][1], alpha =0.2, width = 0.3, color = colors[index], edgecolor = 'k')
            index += 1
            x_label_pos.append(pos)
            pos += 0.5

        # for i,j in enumerate(ax1.lines):
        #     j.set_color(colors[i])

        # ax1.legend(SCHEMES_REW, loc='best')
        
        plt.ylabel('Time (s)')
        ax1.set_xticks(x_label_pos)
        ax1.set_xticklabels(data_x)
        # plt.xticks(fontsize = 16)
        ax1.spines['top'].set_visible(False)
        ax1.spines['right'].set_visible(False)
        plt.title('Running tasks (timestamps:' + str('%.3f'% time_stamp) + 's)')
        ax1.spines['bottom'].set_linewidth(2.5)
        ax1.spines['left'].set_linewidth(2.5)
        # plt.grid()

        ax2 = fig.add_subplot(312)
        data_x = JOB
        data_y = []
        # SCHEMES_REW = []
        for job in JOB:
            max_value = 0
            for task in task_executed:
                if task_executed[task][2] == job:
                    if task_executed[task][0] >= max_value:
                        max_value = task_executed[task][0]
                    # data_x.append(task + ':DC' + str(task_current[task][1]))
                    # data_y.append(task_current[task][0])
                    # SCHEMES_REW.append(task + ':' + 'DC' + str(task_current[task][1]))
            data_y.append(max_value)
        # ax1.plot(data_x, data_y)
        colors = [COLOR_MAP(i) for i in np.linspace(0, 1, len(data_x))]
        pos = 0.5
        index = 0
        x_label_pos = []
        for task in data_x:
            plt.bar(pos, data_y[index], alpha =0.8, width = 0.3, color = colors[index], edgecolor = 'k')
            index += 1
            x_label_pos.append(pos)
            pos += 0.5

        # for i,j in enumerate(ax1.lines):
        #     j.set_color(colors[i])

        # ax1.legend(SCHEMES_REW, loc='best')
        
        plt.ylabel('Time (s)') #'Time (s)'
        ax2.set_xticks(x_label_pos)
        ax2.set_xticklabels(data_x)
        # plt.xticks(fontsize = 16)
        ax2.spines['top'].set_visible(False)
        ax2.spines['right'].set_visible(False)
        plt.title('Completion time of jobs (current)')
        ax2.spines['bottom'].set_linewidth(2.5)
        ax2.spines['left'].set_linewidth(2.5)


        ax3 = fig.add_subplot(313)
        data_x = JOB
        data_y = []
        # SCHEMES_REW = []
        for job in JOB:
            data_y.append(jobs_current_task[job])
            # max_value = 0
            # for task in task_executed:
            #     if task_executed[task][2] == job:
            #         if task_executed[task][0] >= max_value:
            #             max_value = task_executed[task][0]
                    # data_x.append(task + ':DC' + str(task_current[task][1]))
                    # data_y.append(task_current[task][0])
                    # SCHEMES_REW.append(task + ':' + 'DC' + str(task_current[task][1]))
            # data_y.append(max_value)
        # ax1.plot(data_x, data_y)
        colors = [COLOR_MAP(i) for i in np.linspace(0, 1, len(data_x))]
        pos = 0.5
        index = 0
        x_label_pos = []
        for task in data_x:
            plt.bar(pos, data_y[index], alpha =0.8, width = 0.3, color = colors[index], edgecolor = 'k')
            index += 1
            x_label_pos.append(pos)
            pos += 0.5

        # for i,j in enumerate(ax1.lines):
        #     j.set_color(colors[i])

        # ax1.legend(SCHEMES_REW, loc='best')
        
        plt.ylabel('Time (s)')
        ax3.set_xticks(x_label_pos)
        ax3.set_xticklabels(data_x)
        # plt.xticks(fontsize = 16)
        ax3.spines['top'].set_visible(False)
        ax3.spines['right'].set_visible(False)
        plt.title('The number of running tasks of the jobs (current)')
        ax3.spines['bottom'].set_linewidth(2.5)
        ax3.spines['left'].set_linewidth(2.5)

        plt.show()


        
        forward_time = 0
        min_exe = 65535
        for task in task_current:
            if task_current[task][0] <= min_exe:
                min_exe = task_current[task][0]
                finish_task_loc = task_current[task][1]
                finish_task_name = task
        forward_time = min_exe
        ########################
        ########################
        #  a task is finished, there must be a slot-free or maybe task-free
        # step 1: push the timeline forward min_exe seconds
        # step 2: push the finished task into task executed, jobs_current_task -1, available_slot_state +1
        # step 3: all remaining time of tasks in task_current substract min_exe
        time_stamp += forward_time
        slot_free = True
        task_free = True
        of_job = task_current[finish_task_name][2]
        completion_time_current = task_current[finish_task_name][3]
        value = task_current.pop(finish_task_name)

        task_executed[finish_task_name] = [time_stamp, finish_task_loc, of_job, time_stamp-completion_time_current]
        jobs_current_task[of_job] -= 1
        available_slot_state[finish_task_loc] += 1
        for task in task_current:
            task_current[task][0] -= forward_time

        if time_stamp > 100:
            Onload = False


            # a = 

    # test = table.row_values(3)
    print('Good night')
    fig = plt.figure()
    ax2 = fig.add_subplot(111)
    data_x = JOB
    data_y = []
    SCHEMES_REW = []
    for job in JOB:
        max_value = 0
        for task in task_executed:
            if task_executed[task][2] == job:
                if task_executed[task][0] >= max_value:
                    max_value = task_executed[task][0]
                # data_x.append(task + ':DC' + str(task_current[task][1]))
                # data_y.append(task_current[task][0])
                # SCHEMES_REW.append(task + ':' + 'DC' + str(task_current[task][1]))
        data_y.append(max_value)
    # ax1.plot(data_x, data_y)
    SCHEMES_REW.append('Average completion time' + ':' + str('%.3f'% np.mean(data_y)) )
    colors = [COLOR_MAP(i) for i in np.linspace(0, 1, len(data_x))]
    pos = 0.5
    index = 0
    x_label_pos = []
    for task in data_x:
        plt.bar(pos, data_y[index], alpha =0.8, width = 0.3, color = colors[index], edgecolor = 'k')
        index += 1
        x_label_pos.append(pos)
        pos += 0.5

    # for i,j in enumerate(ax1.lines):
    #     j.set_color(colors[i])

    ax2.legend(SCHEMES_REW, loc='best')
    
    plt.ylabel('Time (s)', fontsize = 18)
    ax2.set_xticks(x_label_pos)
    ax2.set_xticklabels(data_x)
    plt.xticks(fontsize = 16)
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    plt.title('Completion time of jobs (current)', fontsize = 18)
    ax2.spines['bottom'].set_linewidth(2.5)
    ax2.spines['left'].set_linewidth(2.5)

    plt.show()

    ########################################################



if __name__ == '__main__':
	main()


