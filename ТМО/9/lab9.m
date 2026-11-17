%% Лабораторная работа №9 (SimEvents)
% Однофазная одноканальная СМО M/M/1/10 с ограниченной очередью и обратной связью.
% Рабочая схема SMO_lab9.slx из блоков SimEvents (sldelib), разложенная по
% образцу методички (вариант 18): Entity_Generator -> Path_Combiner -> FIFO_Queue
% -> Service_Server -> Return_Decision -> Return_Buffer (обратная связь) ->
% Completed_Requests; параметры слева, съём статистики через Goto/From + To
% Workspace + Display внизу. Блоки расставлены по координатам (без наложений).
% ИКС-431 Салий Владислав, вариант 18
clear; clc; close all;

mu    = 1;      % интенсивность потока обслуживания
capQ  = 10;     % ёмкость очереди (M/M/1/10)
Tstop = 4000;   % длительность моделирования (с)

fprintf('=== Лабораторная работа №9 (SimEvents) ===\n');
fprintf('M/M/1/%d с ограниченной очередью и обратной связью.\n', capQ);
fprintf('mu=%.2f, ёмкость очереди=%d, время моделирования=%d с\n\n', mu, capQ, Tstop);

% Эксперименты:  lambda  wmax   (p возврата = 0.5 задаётся Return_Decision)
expParams = [ 0.10  1 ;
              0.15  1 ;
              0.20  1 ;
              0.25  1 ;
              0.30  1 ];
pfb = 0.5;

nExp = size(expParams, 1);
R = zeros(nExp, 4);          % A, T_sys, Lq, rho
lastLog = [];

for e = 1:nExp
    res = run_smo9(expParams(e,1), expParams(e,2), pfb, mu, capQ, Tstop, (e==1));
    R(e,:) = [res.A, res.T_sys, res.Lq, res.rho];
    if e==1, lastLog = res; end
    fprintf('--- Эксперимент %d: lambda=%.2f, wmax=%.1f, p=%.2f ---\n', ...
            e, expParams(e,1), expParams(e,2), pfb);
    fprintf('  A = %.4f | T_сист = %.3f | L_оч = %.3f | rho = %.3f\n', ...
            res.A, res.T_sys, res.Lq, res.rho);
    fprintf('  W_оч = %.3f | обслужено = %d | сгенерировано = %d\n\n', ...
            res.Wq, res.arrEnd, res.genEnd);
end

fprintf('================ ТАБЛИЦА 9.1 ================\n');
fprintf(' lambda wmax   p  |    A     T_сист   L_оч   rho\n');
fprintf('-----------------------------------------------\n');
for e = 1:nExp
    fprintf('%6.2f %4.1f %4.2f | %7.4f %8.3f %6.3f %5.3f\n', ...
        expParams(e,1), expParams(e,2), pfb, R(e,1), R(e,2), R(e,3), R(e,4));
end
fprintf('================================================\n\n');

%% Графики динамики (первый эксперимент) — рис. 9.8-9.11
figure('Name','Рис.9.8 Прибытия в СМО','Color','w');
plot(lastLog.genTS.Time, lastLog.genTS.Data, 'b-', 'LineWidth', 1.5); grid on;
xlabel('t, с'); ylabel('N_{вход}'); title('Прибытия заявок (кумулятивно)');

figure('Name','Рис.9.9 Среднее время ожидания','Color','w');
plot(lastLog.WqTS.Time, lastLog.WqTS.Data, 'c-', 'LineWidth', 1.5); grid on;
xlabel('t, с'); ylabel('W_{оч}, с'); title('Среднее время ожидания в очереди');

figure('Name','Рис.9.10 Количество заявок в очереди','Color','w');
stairs(lastLog.qLenTS.Time, lastLog.qLenTS.Data, 'r-', 'LineWidth', 1.3); grid on;
xlabel('t, с'); ylabel('Q(t)'); title('Количество заявок в очереди (в динамике)');

figure('Name','Рис.9.11 Выходы из СМО','Color','w');
plot(lastLog.arrTS.Time, lastLog.arrTS.Data, 'g-', 'LineWidth', 1.5); grid on;
xlabel('t, с'); ylabel('N_{вых}'); title('Выходы (обслуженные) заявок из СМО');

fprintf('Схема модели сохранена: SMO_lab9.slx (откройте в Simulink)\n');
fprintf('=== ЛАБОРАТОРНАЯ РАБОТА №9 (SimEvents) ЗАВЕРШЕНА ===\n');

%% ==================== Функция сборки и запуска ====================
function res = run_smo9(lambda, wmax, pfb, mu, capQ, Tstop, saveModel)
    load_system('sldelib');
    m = 'SMO_lab9';
    if bdIsLoaded(m), close_system(m, 0); end
    new_system(m);

    % ---- Основной поток сущностей (ряд сверху, слева направо) ----
    addb(m,'sldelib/Entity Generator',     'Entity_Generator', [40  70 120 120]);
    addb(m,'sldelib/Entity Input Switch',  'Path_Combiner',    [200 70 245 120]);
    addb(m,'sldelib/Entity Queue',         'FIFO_Queue',       [300 70 360 120]);
    addb(m,'sldelib/Entity Server',        'Service_Server',   [420 70 480 120]);
    addb(m,'sldelib/Entity Output Switch', 'Return_Decision',  [540 70 585 120]);
    addb(m,'sldelib/Entity Terminator',    'Completed_Requests',[720 70 780 110]);
    addb(m,'sldelib/Entity Queue',         'Return_Buffer',    [540 190 600 240]);

    G  = [m '/Entity_Generator'];   PC = [m '/Path_Combiner'];
    Q  = [m '/FIFO_Queue'];         S  = [m '/Service_Server'];
    RD = [m '/Return_Decision'];    RB = [m '/Return_Buffer'];
    CR = [m '/Completed_Requests'];

    % Генератор: экспоненциальный вход; вес увеличивает время обслуживания (st)
    set_param(G,'GenerationMethod','Time-based','TimeSource','Function', ...
        'GenerateEntityAtSimulationStart','on', ...
        'IntergenerationTimeAction',['dt = -log(rand())/' num2str(lambda) ';'], ...
        'AttributeName','st','AttributeInitialValue','1', ...
        'GenerateAction',['st = -log(rand())/' num2str(mu) ' + rand()*' num2str(wmax) ';']);
    set_param(G,'NumberEntitiesDeparted','on');           % out:[count(1), entity(2)]

    set_param(PC,'NumberInputPorts','2','SwitchingCriterion','Round robin');
    set_param(Q,'Capacity',num2str(capQ),'QueueType','FIFO');
    set_param(Q,'NumberEntitiesInBlock','on');            % out:[count(1),Wq(2),Lq(3),entity(4)]
    set_param(Q,'AverageWait','on');
    set_param(Q,'AverageQueueLength','on');
    set_param(S,'Capacity','1','ServiceTimeSource','Attribute','ServiceTimeAttributeName','st');
    set_param(S,'Utilization','on');                      % out:[util(1), entity(2)]
    set_param(RD,'NumberOutputPorts','2','SwitchingCriterion','Equiprobable'); % p=0.5
    set_param(RB,'Capacity',num2str(capQ),'QueueType','FIFO');
    set_param(CR,'NumberEntitiesArrived','on');           % out:[arrCnt(1)]

    % ---- Соединения основного потока ----
    add_line(m,'Entity_Generator/2','Path_Combiner/1');
    add_line(m,'Path_Combiner/1','FIFO_Queue/1');
    add_line(m,'FIFO_Queue/4','Service_Server/1');
    add_line(m,'Service_Server/2','Return_Decision/1');
    add_line(m,'Return_Decision/1','Return_Buffer/1');   % возврат
    add_line(m,'Return_Buffer/1','Path_Combiner/2');
    add_line(m,'Return_Decision/2','Completed_Requests/1'); % выход

    % ---- Параметры (левая колонка) ----
    add_param(m,'Lambda',      num2str(lambda), [40  300 75 330]);
    add_param(m,'N_Queries',   '100',           [40  350 75 380]);
    add_param(m,'Max_Weight',  num2str(wmax),   [40  400 75 430]);
    add_param(m,'Return_Prob', num2str(pfb),    [40  450 75 480]);

    % ---- Интерфейс съёма статистики (Goto/From -> To Workspace -> Display) ----
    add_stat(m,'Entity_Generator',   1,'Arrivals','out_iw9_arr','Display_Arrivals',     200);
    add_stat(m,'FIFO_Queue',         1,'QLen',    'out_iw9_q',  'Display_Average_Queue',320);
    add_stat(m,'FIFO_Queue',         2,'QAvg',    'out_iw9_qavg','',                    440);
    add_stat(m,'FIFO_Queue',         3,'QLenAvg', 'out_iw9_lq', '',                      800);
    add_stat(m,'Service_Server',     1,'Util',    'out_iw9_u',  'Display_Utilization',  560);
    add_stat(m,'Completed_Requests', 1,'DepCnt',  'out_iw9_dep','Display_Departures',   680);

    set_param(m,'StopTime',num2str(Tstop),'Solver','FixedStepDiscrete');
    out = sim(m);

    genTS  = out.get('out_iw9_arr');  qLenTS = out.get('out_iw9_q');
    WqTS   = out.get('out_iw9_qavg'); utilTS = out.get('out_iw9_u');
    arrTS  = out.get('out_iw9_dep');  LqTS   = out.get('out_iw9_lq');

    res.genEnd = genTS.Data(end);
    res.arrEnd = arrTS.Data(end);
    res.Wq     = WqTS.Data(end);
    res.Lq     = LqTS.Data(end);
    res.rho    = utilTS.Data(end);
    res.A      = res.arrEnd / Tstop;
    res.T_sys  = res.Wq + (1/mu + wmax/2);
    res.genTS = genTS; res.arrTS = arrTS; res.qLenTS = qLenTS; res.WqTS = WqTS;

    if saveModel, save_system(m, fullfile(pwd,'SMO_lab9.slx')); end
    close_system(m,0);
end

%% Добавить блок и задать ему позицию
function addb(m, type, name, pos)
    h = add_block(type, [m '/' name]);
    set_param(h, 'Position', pos);
end

%% Стат-порт -> Goto; From -> To Workspace (+ Display). Колонка на x0, снизу.
function add_stat(m, blk, pidx, tag, wsvar, dispname, x0)
    yG = 320; yF = 380; yW = 440; yD = 500;
    gname = ['Goto_' tag];  addb(m,'simulink/Signal Routing/Goto', gname, [x0    yG x0+55 yG+25]);
    set_param([m '/' gname],'GotoTag',tag,'TagVisibility','global');
    fname = ['From_' tag];  addb(m,'simulink/Signal Routing/From', fname, [x0    yF x0+55 yF+25]);
    set_param([m '/' fname],'GotoTag',tag);
    addb(m,'simulink/Sinks/To Workspace', wsvar, [x0-5 yW x0+75 yW+30]);
    set_param([m '/' wsvar],'VariableName',wsvar,'SaveFormat','Timeseries','SampleTime','-1');

    ph  = get_param([m '/' blk],'PortHandles');
    gph = get_param([m '/' gname],'PortHandles');
    fph = get_param([m '/' fname],'PortHandles');
    wph = get_param([m '/' wsvar],'PortHandles');
    add_line(m, ph.Outport(pidx), gph.Inport(1),'autorouting','on');
    add_line(m, fph.Outport(1),   wph.Inport(1),'autorouting','on');
    if ~isempty(dispname)
        addb(m,'simulink/Sinks/Display', dispname, [x0 yD x0+55 yD+25]);
        dph = get_param([m '/' dispname],'PortHandles');
        add_line(m, fph.Outport(1), dph.Inport(1),'autorouting','on');
    end
end

%% Constant-параметр с отображением
function add_param(m, name, val, pos)
    addb(m,'simulink/Sources/Constant', name, pos);
    set_param([m '/' name],'Value',val);
    d = ['DisplayParam_' name];
    addb(m,'simulink/Sinks/Display', d, [pos(1)+100 pos(2) pos(1)+150 pos(2)+25]);
    cph = get_param([m '/' name],'PortHandles'); dph = get_param([m '/' d],'PortHandles');
    add_line(m, cph.Outport(1), dph.Inport(1),'autorouting','on');
end
