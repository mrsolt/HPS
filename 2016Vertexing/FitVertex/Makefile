all: upperlimit.so testUpper SimpleExample
clean:
	rm upperlimit.so testUpper SimpleExample
upperlimit.so:
	f2py -c -m upperlimit upper.pyf Upper.f UpperLim.f CMaxinf2.f y_vs_CLf.f Cinf.f ConfLev.f CombConf.f C02.f CnMax.f CERN_Stuff2.f
testUpper:
	f77 -o testUpper testUpper.f Upper.f UpperLim.f CMaxinf2.f y_vs_CLf.f Cinf.f ConfLev.f CombConf.f C02.f CnMax.f CERN_Stuff2.f
SimpleExample:
	f77 -o SimpleExample SimpleExample.f UpperLim.f CMaxinf2.f y_vs_CLf.f Cinf.f ConfLev.f C02.f CnMax.f CERN_Stuff2.f
