      Program testUpper
C Find the CL upper limit with methods 1-6 in a MC.  Compile on Linux with
C f77 -g -o testUpper testUpper.f Upper.f C0.f CombConf.f UpperLim.f CnMax.f Cinf.f CMaxinf.f ConfLev.f y_vs_CLf.f CERN_Stuff.f
C Under Linux, and probably Mac OS-X, it's ok to replace "f77 -g" with "gfortran".
      Implicit None
      Integer Maxp1,NMethods
      parameter (Maxp1=500)
      parameter (NMethods=6)
      Real sigmatrue,sigmaMC,points(0:Maxp1,2),mu(2),C0,
     1 Upper,CL,mupersigma(2),FC(0:Maxp1,2),CnMax 
      Integer ITab1(0:11),ITab2(0:11),
     2 ITab1Miss(0:11),ITab2Miss(0:11),ITab(0:11,0:11),
     3 ITabMiss(0:11,0:11)
      Integer I,J,K,Nexp,Nevts(2),ICode,Mistakes(0:NMethods),
     1 Ntrials,K1,K2,mtop,Istat
      Real*8 avgsig(0:NMethods)
      Integer Maxevts
      Parameter (Maxevts=20000)
      Real CL0,mu0(20),xmax(20),f(0:Maxevts,2),p1,p2
      Integer Method0,Nexp0,IFlag0,Nevts0(2)
      Common/UpperCom/Method0,CL0,Nexp0,xmax,mu0,IFlag0,f,Nevts0,
     1 p1,p2
      Ntrials=1000
      Write(6,*) "Give the number of trials, such as", Ntrials
      Read(5,*) Ntrials
      sigmatrue=.25 ! "True" MC cross section
      Write(6,*) "Give the true MC cross section, such as", sigmatrue
      Read(5,*) sigmatrue
      mupersigma(1)=15. !Experiment 1 expected # of events/(unit cross section)
      mupersigma(2)=25.
      CL=0.9
      Write(6,*) "Give the desired confidence level, such as",CL
      Read(5,*) CL
      mu(1)=mupersigma(1)*sigmatrue ! expected number of events in exp. 1
      mu(2)=mupersigma(2)*sigmatrue
      Do I=0,NMethods
        Mistakes(I)=0
        avgsig(I)=0.D0
      EndDo
      Do I=1,Ntrials
         Nexp=2
         Do K=1,Nexp
C Generate random experiments with mu(1) and mu(2) events on the average
           Call pointgen(mu(K),Maxp1,points(0,K),Nevts(K))
           Do J=0,Nevts(K)
C pointgen generates the points from 0 to mu(K).  The distribution should
C be from 0 to 1.
             FC(J,K)=points(J,K)/mu(K)
           EndDo
           Nevts(K)=Nevts(K)-1 ! pointgen counts the endpoint in Nevts
         EndDo
         Do J=0,NMethods
           If(J.eq.0) Then
              Nexp=1
           Else
              Nexp=2
           EndIf
           K=J
C           If(J.eq.3) K=-J
           sigmaMC=Upper(K,CL,Nexp,Maxp1,Nevts,mupersigma,FC,ICode)
C
C There should be about 1/10 as many mistakes as trials for CL=0.9,
C where a "mistake" is when the upper limit is below the true value.  But
C if sigmatrue is too small, even zero events in experiments must give
C an upper limit above sigmatrue, and there will be no "mistakes".  For
C somewhat small sigmatrue, there will be some mistakes, but fewer than 10%.
C
           If(sigmaMC.lt.sigmatrue) Then
              Mistakes(J)=Mistakes(J)+1
           EndIf
           avgsig(J)=avgsig(J)+sigmaMC
         EndDo
      EndDo
      Do I=0,NMethods
         avgsig(I)=avgsig(I)/(sigmatrue*float(Ntrials))
      EndDo
      Write(6,10) Mistakes,Ntrials,avgsig
 10   Format(7I6,' mistakes out of',I7,' trials, with avg/true',7F7.3)
      Stop
      End
      Subroutine pointgen(MEAN,NMAX,point,Npoints)
C Given "Mean" = expectation value of the number of events in an interval,
C produce point(0:Npoints), with point(0)=0., point(Npoints)=Mean. Step through
C the interval (0,Mean) starting at 0 and incrementing by Delta distributed
C according to an exponential decay with unit length.  The resulting set of
C hits represents a sample of what one would find from random events uniformly
C distributed with mean total number Mean.  Since the routine stores all points
C during its operation, Mean had better be well under NMAX.
C
C This routine uses CERNLIB's RANLUX
      Implicit None
      Real Mean
      Integer NMAX,NPoints,I
      Real Point(0:NMAX), Random(1)
      Point(0)=0.
      NPoints=0
C First generate NPoints points between 0 and Mean.  NPoints better be < NMAX.
      Do I=1,NMAX
        Call RANLUX(Random,1)
        Point(I)=Point(I-1)-log(Random(1))
        If(Point(I).gt.Mean) Then
           NPoints=I
           Point(I)=Mean
           Return
        EndIf
      EndDo
      Write(6,*) "Too many points.  Give up."
      Stop
      End
