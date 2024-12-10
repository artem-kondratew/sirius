MODULE Module_TCIP
    
    RECORD msg
        num id_wobj2;
        pose wobj2;
    ENDRECORD
    
    RECORD msg_com1
        num id1;
        pos trans_target1;
        orient rot_target1;
    ENDRECORD
    
    RECORD msg_com2
        num id2;
        pos trans_target2;
        orient rot_target2;
    ENDRECORD
    
    RECORD msg_com3
        num id3;
        pos trans_target3;
        orient rot_target3;
    ENDRECORD
    
    VAR msg wobj_plate;
    VAR msg_com1 component1;
    VAR msg_com2 component2;
    VAR msg_com3 component3;
    
    VAR bool ok;
    VAR bool ok1;
    VAR bool ok2;
    VAR bool ok3;
    
    VAR num id_wobj;
    
    PERS tooldata pen:=[TRUE,[[0,0,139],[1,0,0,0]],[0.5,[0,0,20],[1,0,0,0],0,0,0]];
    CONST robtarget home:=[[-38.34,-777.7,785.02],[0,-1,0,0],[0,-1,0,0],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
	PERS tooldata toolGripper:=[TRUE,[[0,0,160],[1,0,0,0]],[0.8,[0,0,1],[1,0,0,0],0,0,0]];
    
    TASK PERS wobjdata wobj2:=[FALSE,TRUE,"",[[747.33,-871.732,730.071],[1,0,0,0]],[[0,0,0],[1,0,0,0]]];
    TASK PERS wobjdata wobj1:=[FALSE,TRUE,"",[[-38.6576,-878.124,321.314],[0.708333,0,0,-0.705878]],[[0,0,0],[1,0,0,0]]];
    
    VAR robtarget Target_1:=[[832.033208884,64.441917195,766.321123591],[0.000000023,-0.008694109,0.999962206,0.000000001],[0,-1,0,0],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    VAR robtarget Target_2:=[[832.033208884,64.441917195,766.321123591],[0.000000023,-0.008694109,0.999962206,0.000000001],[0,-1,0,0],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    VAR robtarget Target_3:=[[832.033208884,64.441917195,766.321123591],[0.000000023,-0.008694109,0.999962206,0.000000001],[0,-1,0,0],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    
    VAR robtarget Target_t0:=[[141.46,-43.28,7.51],[0.0238823,-0.71662,-0.695825,0.0147844],[0,-1,0,0],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    VAR robtarget Target_t1:=[[169.43,-154.69,9.96],[0.0238823,-0.71662,-0.695825,0.0147844],[0,-1,0,0],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    VAR robtarget Target_t2:=[[69.2,-169.1,26.45],[0.0242625,-0.51569,-0.856417, -0.000501611],[0,-1,0,0],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    
    VAR socketdev serverSocket;
    VAR socketdev clientSocket;
    VAR string data;
    
    VAR string str1:="";
    VAR msg Pack;
    
    VAR string str2:="";
    VAR msg_com1 Pack1;
    
    VAR string str3:="";
    VAR msg_com2 Pack2;
    
    VAR string str4:="";
    VAR msg_com3 Pack3;
    
    PROC main()
        SocketCreate serverSocket;
        
        SocketBind serverSocket, "192.168.125.1", 5000;
        SocketListen serverSocket;
        
        SocketAccept serverSocket, clientSocket, \Time:=WAIT_MAX;
            
        SocketReceive clientSocket \Str:=str1;
        TPWrite str1;
        SocketReceive clientSocket \Str:=str2;
        TPWrite str2;
        SocketReceive clientSocket \Str:=str3;
        TPWrite str3;
        SocketReceive clientSocket \Str:=str4;
        TPWrite str4;
        
        SocketSend clientSocket \Str:="Coordinates received";
           
        SocketClose clientSocket;
        SocketClose serverSocket;
        
        ok:= StrToVal(str1,Pack);
        ok2:= StrToVal(str2,Pack1);
        ok3:= StrToVal(str3,Pack2);
        ok3:= StrToVal(str4,Pack3);
        
        wobj_plate := Pack;
        component1 := Pack1;
        component2 := Pack2;
        component3 := Pack3;
        
        id_wobj := wobj_plate.id_wobj2;
        
        wobj2.oframe := wobj_plate.wobj2;
        
        Target_1.trans := component1.trans_target1;
        Target_1.rot := component1.rot_target1;
        
        Target_2.trans := component2.trans_target2;
        Target_2.rot := component2.rot_target2;
        
        Target_3.trans := component3.trans_target3;
        Target_3.rot := component3.rot_target3;
        
        go_Home;
        move_comp;
        
    ENDPROC
    
    PROC move_comp()
        
        IF component1.id1 = 0 THEN
            open_grip;
            Target_1.trans.z := 160;
            MoveJ Target_1,v100,fine,toolGripper\WObj:=wobj1;
            Target_1.trans.z := 17;
            close_grip;
            MoveJ Target_1,v100,fine,toolGripper\WObj:=wobj1;
            Target_1.trans.z := 160;
            MoveJ Target_1,v100,fine,toolGripper\WObj:=wobj1;
            
            Target_t0.trans.z := 160;
            MoveJ Target_t0,v100,fine,toolGripper\WObj:=wobj2; 
           
            Target_t0.trans.z := 22;
            MoveJ Target_t0,v100,fine,toolGripper\WObj:=wobj2;
            open_grip;
            Target_t0.trans.z := 160;
            MoveJ Target_t0,v100,fine,toolGripper\WObj:=wobj2;
            
        
        ELSEIF component1.id1 = 1 THEN 
            open_grip;
            Target_1.trans.z := 160;
            MoveJ Target_1,v100,fine,toolGripper\WObj:=wobj1;
            Target_1.trans.z := 17;
            close_grip;
            MoveJ Target_1,v100,fine,toolGripper\WObj:=wobj1;
            Target_1.trans.z := 160;
            MoveJ Target_1,v100,fine,toolGripper\WObj:=wobj1;
            
            Target_t1.trans.z := 160;
            MoveJ Target_t1,v100,fine,toolGripper\WObj:=wobj2; 
           
            Target_t1.trans.z := 22;
            MoveJ Target_t1,v100,fine,toolGripper\WObj:=wobj2;
            open_grip;
            Target_t1.trans.z := 160;
            MoveJ Target_t1,v100,fine,toolGripper\WObj:=wobj2;
            
        ELSEIF component1.id1 = 2 THEN 
            open_grip;
            Target_1.trans.z := 160;
            MoveJ Target_1,v100,fine,toolGripper\WObj:=wobj1;
            Target_1.trans.z := 28;
            MoveJ Target_1,v100,fine,toolGripper\WObj:=wobj1;
            close_grip;
            Target_1.trans.z := 160;
            MoveJ Target_1,v100,fine,toolGripper\WObj:=wobj1;
            
            Target_t2.trans.z := 160;
            MoveJ Target_t2,v100,fine,toolGripper\WObj:=wobj2; 
           
            Target_t2.trans.z := 30;
            MoveJ Target_t2,v100,fine,toolGripper\WObj:=wobj2;
            open_grip;
            Target_t2.trans.z := 160;
            MoveJ Target_t2,v100,fine,toolGripper\WObj:=wobj2;
        ENDIF
            
            
        IF component2.id2 = 0 THEN
            open_grip;
            Target_2.trans.z := 160;
            MoveJ Target_2,v100,fine,toolGripper\WObj:=wobj1;
            Target_2.trans.z := 17;
            MoveJ Target_2,v100,fine,toolGripper\WObj:=wobj1;
            close_grip;
            Target_2.trans.z := 160;
            MoveJ Target_2,v100,fine,toolGripper\WObj:=wobj1;
            
            Target_t0.trans.z := 160;
            MoveJ Target_t0,v100,fine,toolGripper\WObj:=wobj2; 
           
            Target_t0.trans.z := 22;
            MoveJ Target_t0,v100,fine,toolGripper\WObj:=wobj2;
            open_grip;
            Target_t0.trans.z := 160;
            MoveJ Target_t0,v100,fine,toolGripper\WObj:=wobj2;
        
        ELSEIF component2.id2 = 1 THEN 
            open_grip;
            Target_2.trans.z := 160;
            MoveJ Target_2,v100,fine,toolGripper\WObj:=wobj1;
            Target_2.trans.z := 17;
            MoveJ Target_2,v100,fine,toolGripper\WObj:=wobj1;
            close_grip;
            Target_2.trans.z := 160;
            MoveJ Target_2,v100,fine,toolGripper\WObj:=wobj1;
            
            Target_t1.trans.z := 160;
            MoveJ Target_t1,v100,fine,toolGripper\WObj:=wobj2; 
           
            Target_t1.trans.z := 22;
            MoveJ Target_t1,v100,fine,toolGripper\WObj:=wobj2;
            open_grip;
            Target_t1.trans.z := 160;
            MoveJ Target_t1,v100,fine,toolGripper\WObj:=wobj2;
            
        ELSEIF component2.id2 = 2 THEN 
            open_grip;
            Target_2.trans.z := 160;
            MoveJ Target_2,v100,fine,toolGripper\WObj:=wobj1;
            Target_2.trans.z := 27;
            MoveJ Target_2,v100,fine,toolGripper\WObj:=wobj1;
            close_grip;
            Target_2.trans.z := 160;
            MoveJ Target_2,v100,fine,toolGripper\WObj:=wobj1;
            
            Target_t2.trans.z := 160;
            MoveJ Target_t2,v100,fine,toolGripper\WObj:=wobj2; 
           
            Target_t2.trans.z := 30;
            MoveJ Target_t2,v100,fine,toolGripper\WObj:=wobj2;
            open_grip;
            Target_t2.trans.z := 160;
            MoveJ Target_t2,v100,fine,toolGripper\WObj:=wobj2;
        ENDIF
            
        IF component3.id3 = 0 THEN
            open_grip;
            Target_3.trans.z := 160;
            MoveJ Target_3,v100,fine,toolGripper\WObj:=wobj1;
            Target_3.trans.z := 17;
            MoveJ Target_3,v100,fine,toolGripper\WObj:=wobj1;
            close_grip;
            Target_3.trans.z := 160;
            MoveJ Target_3,v100,fine,toolGripper\WObj:=wobj1;
            
            Target_t0.trans.z := 160;
            MoveJ Target_t0,v100,fine,toolGripper\WObj:=wobj2; 
           
            Target_t0.trans.z := 22;
            MoveJ Target_t0,v100,fine,toolGripper\WObj:=wobj2;
            open_grip;
            Target_t0.trans.z := 160;
            MoveJ Target_t0,v100,fine,toolGripper\WObj:=wobj2;
        
        ELSEIF component3.id3 = 1 THEN 
            open_grip;
            Target_3.trans.z := 160;
            MoveJ Target_3,v100,fine,toolGripper\WObj:=wobj1;
            Target_3.trans.z := 17;
            MoveJ Target_3,v100,fine,toolGripper\WObj:=wobj1;
            close_grip;
            Target_3.trans.z := 160;
            MoveJ Target_3,v100,fine,toolGripper\WObj:=wobj1;
            
            Target_t1.trans.z := 160;
            MoveJ Target_t1,v100,fine,toolGripper\WObj:=wobj2; 
           
            Target_t1.trans.z := 22;
            MoveJ Target_t1,v100,fine,toolGripper\WObj:=wobj2;
            open_grip;
            Target_t1.trans.z := 160;
            MoveJ Target_t1,v100,fine,toolGripper\WObj:=wobj2;
            
        ELSEIF component3.id3 = 2 THEN 
            open_grip;
            Target_3.trans.z := 160;
            MoveJ Target_3,v100,fine,toolGripper\WObj:=wobj1;
            Target_3.trans.z := 27;
            MoveJ Target_3,v100,fine,toolGripper\WObj:=wobj1;
            close_grip;
            Target_3.trans.z := 160;
            MoveJ Target_3,v100,fine,toolGripper\WObj:=wobj1;
            
            Target_t2.trans.z := 160;
            MoveJ Target_t2,v100,fine,toolGripper\WObj:=wobj2; 
           
            Target_t2.trans.z := 30;
            MoveJ Target_t2,v100,fine,toolGripper\WObj:=wobj2;
            open_grip; 
            Target_t2.trans.z := 160;
            MoveJ Target_t2,v100,fine,toolGripper\WObj:=wobj2; 
           
            
        ENDIF
        
    ENDPROC
    
    PROC open_grip()
	    PulseDO\High,do_GripOpen;
	    WaitTime 0.5;
	    WaitDI di_GripOpened,1;
	ENDPROC
    
    PROC close_grip()
        PulseDO\High,do_GripClose;
        WaitTime 0.5;
        WaitDI di_GripClosed,1;
    ENDPROC
    
    PROC go_Home()
        MoveJ home,v100,fine,toolGripper\WObj:=wobj0;
	ENDPROC
    
ENDMODULE
