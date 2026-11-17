%% Лабораторная работа №10 (SimEvents)
% Имитационная модель СМО с общей очередью M/M/c (единая FIFO-очередь, c каналов).
% Цепочка SimEvents: Entity Generator -> Entity Queue -> Entity Server (c серверов)
% -> Entity Terminator. Статистика снимается с портов блоков.
% ИКС-431 Салий Владислав, вариант 18
clear; clc; close all;

mu   = 1;      % интенсивность обслуживания одного канала
c    = 3;      % число каналов (серверов)
capQ = 100;    % ёмкость общей очереди
Tstop = 4000;  % длительность моделирования

fprintf('=== Лабораторная работа №10 (SimEvents) ===\n');
fprintf('СМО с общей очередью M/M/%d. mu=%.2f, c=%d, ёмкость очереди=%d\n\n', c, mu, c, capQ);

lambda_list = [0.5 1.0 1.5 2.0 2.5];
nExp = numel(lambda_list);
R = zeros(nExp,5);   % A, W, T, Lq, util
lastLog = [];
for e = 1:nExp
    res = run_smo10(lambda_list(e), mu, c, capQ, Tstop, (e==nExp));
    R(e,:) = [res.A, res.Wq, res.T_sys, res.Lq, res.util];
    if e==nExp, lastLog=res; end
    [Lq_th, T_th] = erlangC(lambda_list(e), mu, c);
    fprintf('lambda=%.2f (rho=%.3f): A=%.4f  W_оч=%.4f  T_сист=%.4f  L_оч=%.4f  util=%.4f | Эрланг T=%.4f Lq=%.4f\n', ...
        lambda_list(e), lambda_list(e)/(c*mu), res.A, res.Wq, res.T_sys, res.Lq, res.util, T_th, Lq_th);
end

fprintf('\n================= ИТОГОВАЯ ТАБЛИЦА =================\n');
fprintf(' lambda  rho  |    A      W      T      Lq    util\n');
fprintf('--------------------------------------------------\n');
for e=1:nExp
    fprintf('%6.2f %5.3f | %6.3f %6.3f %6.3f %6.3f %6.3f\n', ...
        lambda_list(e), lambda_list(e)/(c*mu), R(e,1),R(e,2),R(e,3),R(e,4),R(e,5));
end
fprintf('==================================================\n');

%% Графики динамики (последний эксперимент)
figure('Name','Рис.10 Прибытия','Color','w');
plot(lastLog.genTS.Time,lastLog.genTS.Data,'b-','LineWidth',1.5); grid on;
xlabel('t, c'); ylabel('N_{вход}'); title('Прибытия заявок в СМО с общей очередью');

figure('Name','Рис.10 Средняя длина очереди','Color','w');
plot(lastLog.LqTS.Time,lastLog.LqTS.Data,'m-','LineWidth',1.5); grid on;
xlabel('t, c'); ylabel('L_{оч}'); title('Средняя длина общей очереди');

figure('Name','Рис.10 Загрузка каналов','Color','w');
plot(lastLog.utilTS.Time,lastLog.utilTS.Data,'k-','LineWidth',1.5); grid on;
xlabel('t, c'); ylabel('util'); title('Коэффициент загрузки каналов');

figure('Name','Рис.10 Выходы','Color','w');
plot(lastLog.arrTS.Time,lastLog.arrTS.Data,'g-','LineWidth',1.5); grid on;
xlabel('t, c'); ylabel('N_{вых}'); title('Выходы (обслуженные) заявок');

fprintf('Модель сохранена: SMO_lab10.slx\n');
fprintf('=== ЛАБОРАТОРНАЯ РАБОТА №10 (SimEvents) ЗАВЕРШЕНА ===\n');

%% ==================== Функция сборки и запуска ====================
function res = run_smo10(lambda, mu, c, capQ, Tstop, saveModel)
    load_system('sldelib');
    m = 'SMO_lab10';
    if bdIsLoaded(m), close_system(m,0); end
    new_system(m);

    G=[m '/G']; Q=[m '/Q']; S=[m '/S']; T=[m '/T'];
    add_block('sldelib/Entity Generator',G);  set_param(G,'Position',[40  70 120 120]);
    add_block('sldelib/Entity Queue',Q);      set_param(Q,'Position',[200 70 270 120]);
    add_block('sldelib/Entity Server',S);     set_param(S,'Position',[350 70 420 120]);
    add_block('sldelib/Entity Terminator',T); set_param(T,'Position',[500 70 560 110]);

    set_param(G,'GenerationMethod','Time-based','TimeSource','Function', ...
        'GenerateEntityAtSimulationStart','on', ...
        'IntergenerationTimeAction',['dt = -log(rand())/' num2str(lambda) ';'], ...
        'AttributeName','st','AttributeInitialValue','1', ...
        'GenerateAction',['st = -log(rand())/' num2str(mu) ';']);
    set_param(G,'NumberEntitiesDeparted','on');          % out:[count(1),entity(2)]

    set_param(Q,'Capacity',num2str(capQ),'QueueType','FIFO');
    set_param(Q,'AverageWait','on'); set_param(Q,'AverageQueueLength','on'); % out:[Wq(1),Lq(2),entity(3)]

    set_param(S,'Capacity',num2str(c), ...               % c серверов = общая очередь
              'ServiceTimeSource','Attribute','ServiceTimeAttributeName','st');
    set_param(S,'Utilization','on');                     % out:[util(1),entity(2)]

    set_param(T,'NumberEntitiesArrived','on');           % out:[arrCnt(1)]

    % поток сущностей (сущность = последний outport)
    add_line(m,'G/2','Q/1'); add_line(m,'Q/3','S/1'); add_line(m,'S/2','T/1');

    % статистика -> To Workspace
    addTW(m,'G',1,'genTS',40);  addTW(m,'Q',1,'WqTS',160);  addTW(m,'Q',2,'LqTS',280);
    addTW(m,'S',1,'utilTS',400); addTW(m,'T',1,'arrTS',520);

    set_param(m,'StopTime',num2str(Tstop),'Solver','FixedStepDiscrete');
    out = sim(m);

    genTS=out.get('genTS'); WqTS=out.get('WqTS'); LqTS=out.get('LqTS');
    utilTS=out.get('utilTS'); arrTS=out.get('arrTS');
    res.A = arrTS.Data(end)/Tstop;
    res.Wq = WqTS.Data(end);
    res.Lq = LqTS.Data(end);
    res.util = utilTS.Data(end);
    res.T_sys = res.Wq + 1/mu;
    res.genTS=genTS; res.arrTS=arrTS; res.LqTS=LqTS; res.utilTS=utilTS;

    if saveModel, save_system(m, fullfile(pwd,'SMO_lab10.slx')); end
    close_system(m,0);
end

function addTW(m, blk, pidx, varn, x0)
    to=[m '/TW_' varn]; add_block('simulink/Sinks/To Workspace', to);
    set_param(to,'Position',[x0 200 x0+80 230]);
    set_param(to,'VariableName',varn,'SaveFormat','Timeseries','SampleTime','-1');
    ph=get_param([m '/' blk],'PortHandles'); toph=get_param(to,'PortHandles');
    add_line(m, ph.Outport(pidx), toph.Inport(1),'autorouting','on');
end

function [Lq, T_sys] = erlangC(lambda, mu, c)
    rho = lambda/(c*mu);
    if rho>=1, Lq=Inf; T_sys=Inf; return; end
    a = lambda/mu; s=0;
    for kk=0:c-1, s=s+a^kk/factorial(kk); end
    p0 = 1/(s + a^c/(factorial(c)*(1-rho)));
    Lq = (a^c*rho)/(factorial(c)*(1-rho)^2)*p0;
    T_sys = Lq/lambda + 1/mu;
end
