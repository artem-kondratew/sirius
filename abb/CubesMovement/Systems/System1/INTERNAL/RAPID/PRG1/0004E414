MODULE Module1
	CONST robtarget home:=[[944.855715851,0,1074],[0.5,0,0.866025404,0],[0,0,0,0],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
	CONST robtarget cube_1_contact:=[[115,15,15],[0,0.707106781,0.707106781,0],[0,0,0,0],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
	CONST robtarget safe_pose:=[[0.000003222,0.000000245,246.376418077],[0,0.707106781,0.707106781,0],[-1,-1,0,0],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
	CONST robtarget target_1:=[[0,15,15],[0,0.707106781,0.707106781,0],[0,0,0,0],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
	CONST robtarget cube_2_contact:=[[215,15,15],[0,0.707106781,0.707106781,0],[0,0,0,0],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
	CONST robtarget target_2:=[[0,15,45],[0,0.707106781,0.707106781,0],[0,0,0,0],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
	CONST robtarget cube_3_contact:=[[315,15,15],[0,0.707106781,0.707106781,0],[0,0,0,0],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
	CONST robtarget target_3:=[[0,15,75],[0,0.707106781,0.707106781,0],[0,0,0,0],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    !***********************************************************
    !
    ! Module:  Module1
    !
    ! Description:
    !   <Insert description here>
    !
    ! Author: user
    !
    ! Version: 1.0
    !
    !***********************************************************
    
    
    !***********************************************************
    !
    ! Procedure main
    !
    !   This is the entry point of your program
    !
    !***********************************************************
    PROC main()
		go_home;
		move_cube_1;
		move_cube_2;
		move_cube_3;
		wait;
		return_cube_3;
		return_cube_2;
		return_cube_1;
		go_home;
        !Add your code here
    ENDPROC
	PROC go_home()
	    MoveJ home,v100,fine,toolGripper\WObj:=wobj0;
	ENDPROC
	PROC move_cube_1()
	    MoveJ cube_1_contact,v100,fine,toolGripper\WObj:=wobjTable;
	    PulseDO\High,do_GripClose;
	    PulseDO\High,close_cube_1_f;
        WaitTime 1;
	    MoveJ safe_pose,v100,fine,toolGripper\WObj:=wobjTable;
	    MoveL target_1,v100,fine,toolGripper\WObj:=wobjTable;
	    PulseDO\High,do_GripOpen;
	    PulseDO\High,open_cube_1_f;
        WaitTime 1;
	    MoveL safe_pose,v100,fine,toolGripper\WObj:=wobjTable;
	ENDPROC
	PROC move_cube_2()
	    MoveJ cube_2_contact,v100,fine,toolGripper\WObj:=wobjTable;
	    PulseDO\High,do_GripClose;
	    PulseDO\High,close_cube_2_f;
        WaitTime 1;
	    MoveJ safe_pose,v100,fine,toolGripper\WObj:=wobjTable;
	    MoveL target_2,v100,fine,toolGripper\WObj:=wobjTable;
	    PulseDO\High,do_GripOpen;
	    PulseDO open_cube_2_f;
        WaitTime 1;
	    MoveL safe_pose,v100,fine,toolGripper\WObj:=wobjTable;
	ENDPROC
	PROC move_cube_3()
	    MoveJ cube_3_contact,v100,fine,toolGripper\WObj:=wobjTable;
	    PulseDO\High,do_GripClose;
	    PulseDO\High,close_cube_3_f;
        WaitTime 1;
	    MoveJ safe_pose,v100,fine,toolGripper\WObj:=wobjTable;
	    MoveL target_3,v100,fine,toolGripper\WObj:=wobjTable;
	    PulseDO\High,do_GripOpen;
	    PulseDO\High,open_cube_3_f;
        WaitTime 1;
	    MoveL safe_pose,v100,fine,toolGripper\WObj:=wobjTable;
	ENDPROC
	PROC return_cube_1()
	    MoveL target_1,v100,fine,toolGripper\WObj:=wobjTable;
	    PulseDO\High,do_GripClose;
	    PulseDO\High,close_cube_1_b;
        WaitTime 1;
	    MoveL safe_pose,v100,fine,toolGripper\WObj:=wobjTable;
	    MoveJ cube_1_contact,v100,fine,toolGripper\WObj:=wobjTable;
	    PulseDO\High,do_GripOpen;
	    PulseDO\High,open_cube_1_b;
        WaitTime 1;
	    MoveJ safe_pose,v100,fine,toolGripper\WObj:=wobjTable;
	ENDPROC
	PROC return_cube_2()
	    MoveL target_2,v100,fine,toolGripper\WObj:=wobjTable;
	    PulseDO\High,do_GripClose;
	    PulseDO\High,close_cube_2_b;
        WaitTime 1;
	    MoveL safe_pose,v100,fine,toolGripper\WObj:=wobjTable;
	    MoveJ cube_2_contact,v100,fine,toolGripper\WObj:=wobjTable;
	    PulseDO\High,do_GripOpen;
	    PulseDO\High,open_cube_2_b;
        WaitTime 1;
	    MoveJ safe_pose,v100,fine,toolGripper\WObj:=wobjTable;
	ENDPROC
	PROC return_cube_3()
	    MoveL target_3,v100,fine,toolGripper\WObj:=wobjTable;
	    PulseDO\High,do_GripClose;
	    PulseDO\High,close_cube_3_b;
        WaitTime 1;
	    MoveL safe_pose,v100,fine,toolGripper\WObj:=wobjTable;
	    MoveJ cube_3_contact,v100,fine,toolGripper\WObj:=wobjTable;
	    PulseDO\High,do_GripOpen;
	    PulseDO open_cube_3_b;
        WaitTime 1;
	    MoveJ safe_pose,v100,fine,toolGripper\WObj:=wobjTable;
	ENDPROC
	PROC wait()
	    WaitTime 2;
	ENDPROC
ENDMODULE