#define error -1;

init {
	chan ch1 = [0] of {int, int, int};
	chan ch2 = [0] of {int, int, int};
	run Sender (1,1,ch1);
	run Network(ch1, ch2);
	run Receiver(ch2);
}

proctype Sender (int sender; int receiver; chan ch) {
	int datanr = 0;
	int confirm;
	
	do
	:: (datanr < 10) ->
		ch! sender,receiver,datanr;
		if
		:: timeout -> ch! sender,receiver,datanr;
		:: ch? sender,receiver,confirm; datanr = confirm;
		fi;
		
		
	:: else -> break
	od
}
	
proctype Network (chan ch1; chan ch2) {
	int sender;
	int receiver;
	int data;
	chan chout;
	int end;

	/* èim jedan primi, odmah proslijedi!!! */	
	do
	      ::if
		:: ch1?sender,receiver,data; chout = ch2
		:: ch2?sender,receiver,data; chout = ch1
	      fi;
	
	      if	
	      ::chout!sender,receiver,data;
	      ::chout!sender,receiver,data;
	      ::(data!=10) -> skip
	      fi;

	      if
	      :: (data==10) -> break
	      :: else -> skip
	      fi;	

	od

}

proctype Receiver (chan ch) {
	int sender;
	int receiver;
	int datanr=0;

	do
	:: (datanr < 10) ->
		ch? sender,receiver,datanr;			
		datanr = datanr + 1;
		ch! sender,receiver,datanr;			
	:: else -> break
	od
}
