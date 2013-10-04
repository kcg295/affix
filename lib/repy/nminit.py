""" 
Author: Justin Cappos

Module: Node Manager initializer.   It initializes the state needed to run the
        node manager on the local node.   This would most likely be run by the
        installer.

Start date: September 10rd, 2008

This initializes the node manager for Seattle.   It sets up the starting 
resources, creates a configuration file, etc.

The design goals of this version are to be secure, simple, and reliable (in 
that order).   

"""
from repyportability import *
_context = locals()
add_dy_support(_context)

# need to generate a public key
dy_import_module_symbols('rsa.repy')

# need randomfloat...
import random
randomfloat = random.random


import os

import persist

import shutil

import glob

# embedded here.   Is this really the right thing to do?
justinpubkey = {'e':22599311712094481841033180665237806588790054310631222126405381271924089573908627143292516781530652411806621379822579071415593657088637116149593337977245852950266439908269276789889378874571884748852746045643368058107460021117918657542413076791486130091963112612854591789518690856746757312472362332259277422867, 'n':12178066700672820207562107598028055819349361776558374610887354870455226150556699526375464863913750313427968362621410763996856543211502978012978982095721782038963923296750730921093699612004441897097001474531375768746287550135361393961995082362503104883364653410631228896653666456463100850609343988203007196015297634940347643303507210312220744678194150286966282701307645064974676316167089003178325518359863344277814551559197474590483044733574329925947570794508677779986459413166439000241765225023677767754555282196241915500996842713511830954353475439209109249856644278745081047029879999022462230957427158692886317487753201883260626152112524674984510719269715422340038620826684431748131325669940064404757120601727362881317222699393408097596981355810257955915922792648825991943804005848347665699744316223963851263851853483335699321871483966176480839293125413057603561724598227617736944260269994111610286827287926594015501020767105358832476708899657514473423153377514660641699383445065369199724043380072146246537039577390659243640710339329506620575034175016766639538091937167987100329247642670588246573895990251211721839517713790413170646177246216366029853604031421932123167115444834908424556992662935981166395451031277981021820123445253}

ivanpubkey = {'e':6481764711916916397109273726155956377656536637642807312800757546468526438704587962838968130419349372877884749341748111210223731976275154922405947360547743L, 'n':338268226945045594040102034878758444764651534167506742110546096640083709576476389210311132469953959393591066992795836386110112598793559135339292833492240869157982347822379943074587320930881739344852033537843848473043128034075489712546721364258219630002902462839364391703058991174756678850745791050455715522819926432293598770270226759125320092184546422006399480232477970392705428953893948935507551291416633551949790971970309886077216112873834384725916279080756901772364218481535522170812626810368956042592229275686877306681530987143867223127594219058268997365351814588360451088611972783470143103530508782003784668721L}

andreaspubkey = {'e':2822540257849010647923776035626629838287235702704423096484847564654414465000881225428345657955502007283165026369457182106577477435673832705387872492044591, 'n':7882973334996053142664942135950444026685861344481859933376041911948219184913053557765978471764229745595651142694669215028934939643234703102261844806689829406623921142369711977840151829485724053715028017335204594765830956122106406342326605977659034321244220740521419889555563680752118278474604590311585813615909531550891420826960367366865035282430327062985682986212519631866305528935391849319049870616965616088088569190841921248106372804406270878233331052124845608476344647222603275832610760223847946462440120107424978654173015761966334681181665203909859876981557162746876336597081684996911168277402512063104549204937}

brentpubkey = {'e':13320637419729342324775464999050861486620207563289680221497576052388175183061457679807442479774032202586062376188244107037281567734856017246126615397816987, 'n':1664580811888919290322204386558991234618254900951529532302133070531168818003858721747272149690631987748580351955990179501255913110694396600216879077732002470881341935976316877085959939004416255719683229745084259916415734451722865966223832634066289733468156160367733425804203272891858242672578795220978282904336116171736295014176775641186644943132523508056618157857119718575880947188606341972480839706601198399600225860757160583497623882064668962077040113842430719849512995440241391131732067227002145871127232717089191139600707583888074613766713552503609290793641760419007328315145998064258640100176806286961432584093}

carterpubkey = {'e':7168437282876876633529422802762647606914193494803337768799081122185700696756563786082605549299608670375696543059776847908603899996329486965226631637840087, 'n':13724582806519489309968126783922147743627863615598200511401696263542228069378681666246810044371293214491884953122564270345036227213513705482186874644188248345092250636909105502001485885529938258392160401994355515499603431204210994869079065175753824307231699145470453865619794727786444147717765876934692580725863517337863828133103123656377281294656369539247378625499431358002787792903340479787368588244936134498455457634534658784891779316675575606443982304587254557775365931820487291639088098643507354164406035353826606748832467578180697619008125509252740195069184206787138540651467518667460180512988620825126472109931}

armonpubkey = {'e':3200941279173345080519384120021978738782253369732074792477284573335223989343368779528294503375136136053581878735944057988977016652466388720005919328614569, 'n':10553235881745543965137165331102432144225249224999120640550160795651004055141451077300441253063569456659555680900071806944299541573086873371906595419171669228793899400999760006896569579804445778200967916782666825777779527057870748694361762861470028374995168134276333298069549991573308145061643966828157536009984242670282950296031461069582089864549886939538988421709037403953460736874810775713352604046647570646063851167596096553164256127741778276907048527345789544310548454829925324855330039115251074424987130126399705652571956713617760718661078219136803706956075647543263871868993131570886861669612952313210350277323}

cosminpubkey = {'e':7464313175644513168887997744670197216333000296354197242445151519761504998981125780277221724878744115700245550050922885815874909770986351004470139292347799, 'n':5166923677011039755827733929519744979819679623762854241784562417614217033545741940486526418826236364419803842179010374289699995420620924879739633685352210702672742640627499819008012778100349108343082031728623289614040677248497446845750382415953993876705269331334135372972752054447786652022051356046844517168288974483920665154285041052294863296555313446636772615755907095066673797201543950176696075209934813375579921682346075069334926946959040236649186664203325185266985125536978403971085971814812113301555195462618654824626590790622973196762839114686728486351358141165471099773851900314642876491326191107813285382101}


kyungpubkey = {'e':11982834196181141260506010180308270855680653406337235774683333408763963018095300381624627449070255932606419233872822964155179661556140871823461403280265061, 'n':4545103278803184664785828362936668880385736545505423731656699929328390307650054478885855959293582492222118379534939515534504426410706682077004338092024910139743650930741139799450460528199982343120740446388950383095882206034545454151790038610951335439728039864518669360779845402779817426625909179794068292408331048258044602531678529469780131385941771393112498888925305762431363984275516442120381279894993082998112042145269189762889863936169922236763504067652051967137198111570516536122040089214964646207252038973487224346595800354866074385496633452068631506635900294186068046269028804783935234012560912143370854322011}

whitakerpubkey = {'e':10477634680045729170740871005801335641467768434351218193273260736261663260683071190501046740023833805678163947127562567143191763342750947386321129914903107, 'n':44987427972981674752339260202819704730517012150882421722152697507846945597536877512849248015247993496568330468293075099787234124471424993175870958499015752893408423430082235375761053594777621966335657140472558698057752710295102525769733694073754884636247281190665961093377545172427190375844018444884761012112133739252122574732783030450970299506665020988579143717488684873689177064850330080994102560293739679100812859869381904410648772073797463068959999303077023921012354811367752768596219324890425280911356960190242126711549743155477658643884669817671332003188080760023501529565620306559281242446187771479563495411}

kimbrlpubkey = {'e': 12750798911637834184493527277417932326435441532475403800774448739175725604187281847686680376958704258670377931363481008581812321272598098576380537893645661L, 'n': 1694119530377438178605327756918343609642560622450587281085538055601623338006046648422430575979743420720649177376633749707999100479375160182394152499579839724683354585691974439852380416307269958137584031145136607216688365388087428373517454211196220827675163168016261083305774677889141003695384360551834830801509387290263299501085011926406888315285033360312476828837194563160330075556874587331556422111760991448002655062285927283196075326065616510803128158683903383229542721447070637697949343508170520988317745716036498936859443370187163993975449123494153595187542432453684508809154880133201690029687292976773096857649L}



# This is the public key of the person who will control most of the resources.
controllerpubkey = {'e': 1515278400394037168869631887206225761783197636247636149274740854708478416229147500580877416652289990968676310353790883501744269103521055894342395180721167L, 'n': 8811850224687278929671477591179591903829730117649785862652866020803862826558480006479605958786097112503418194852731900367494958963787480076175614578652735061071079458992502737148356289391380249696938882025028801032667062564713111819847043202173425187133883586347323838509679062142786013585264788548556099117804213139295498187634341184917970175566549405203725955179602584979965820196023950630399933075080549044334508921319264315718790337460536601263126663173385674250739895046814277313031265034275415434440823182691254039184953842629364697394327806074576199279943114384828602178957150547925812518281418481896604655037L}



offcutresourcedata ="""# BUG: How do we come up with these values dynamically?
resource cpu .002
resource memory 1000000   # 1 MiB
resource diskused 100000 # .1 MiB
resource events 2
resource filewrite 1000
resource fileread 1000 
resource filesopened 1 
resource insockets 0
resource outsockets 0
resource netsend 0
resource netrecv 0
resource loopsend 0  # would change with prompt functionality (?)
resource looprecv 0
resource lograte 100 # the monitor might log something
resource random 0    # Shouldn't generate random numbers on our own
"""

bigresourcedata = """resource cpu .08
resource memory 100000000   # 100 MiB
resource diskused 80000000 # 80 MiB
resource events 50
resource filewrite 100000
resource fileread 100000
resource filesopened 10
resource insockets 10
resource outsockets 10
resource netsend 100000
resource netrecv 100000
resource loopsend 1000000
resource looprecv 1000000
resource lograte 30000
resource random 100
resource messport 11111
resource messport 12222
resource messport 13333
resource messport 14444
resource messport 15555
resource messport 16666
resource messport 17777
resource messport 18888
resource messport 19999
resource connport 11111
resource connport 12222
resource connport 13333
resource connport 14444
resource connport 15555
resource connport 16666
resource connport 17777
resource connport 18888
resource connport 19999

call gethostbyname_ex allow
call sendmess allow
call recvmess allow
call openconn allow
call waitforconn allow
call stopcomm allow                     # it doesn't make sense to restrict
call socket.close allow                 # let's not restrict
call socket.send allow                  # let's not restrict
call socket.recv allow                  # let's not restrict

# open and file.__init__ both have built in restrictions...
call open allow                         # can read / write
call file.__init__ allow                # can read / write
call file.close allow                   # shouldn't restrict
call file.flush allow                   # they are free to use
call file.next allow                    # free to use as well...
call file.read allow                    # allow read
call file.readline allow                # shouldn't restrict
call file.readlines allow               # shouldn't restrict
call file.seek allow                    # seek doesn't restrict
call file.write allow                   # shouldn't restrict (open restricts)
call file.writelines allow              # shouldn't restrict (open restricts)
call sleep allow                        # harmless
call settimer allow                     # we can't really do anything smart
call canceltimer allow                  # should be okay
call exitall allow                      # should be harmless 

call log.write allow
call log.writelines allow
call getmyip allow                      # They can get the external IP address
call listdir allow                      # They can list the files they created
call removefile allow                   # They can remove the files they create
call randomfloat allow                  # can get random numbers
call getruntime allow                   # can get the elapsed time
call getlock allow                      # can get a mutex
"""

smallresourcedata = """resource cpu .02
resource memory 30000000   # 30 MiB
resource diskused 20000000 # 20 MiB
resource events 15
resource filewrite 100000
resource fileread 100000
resource filesopened 5
resource insockets 5
resource outsockets 5
resource netsend 10000
resource netrecv 10000
resource loopsend 1000000
resource looprecv 1000000
resource lograte 30000
resource random 100
resource messport %s
resource messport %s
resource messport %s
resource messport %s
resource connport %s
resource connport %s
resource connport %s
resource connport %s

call gethostbyname_ex allow
call sendmess allow
call recvmess allow
call openconn allow
call waitforconn allow
call stopcomm allow                     # it doesn't make sense to restrict
call socket.close allow                 # let's not restrict
call socket.send allow                  # let's not restrict
call socket.recv allow                  # let's not restrict

# open and file.__init__ both have built in restrictions...
call open allow                         # can read / write
call file.__init__ allow                # can read / write
call file.close allow                   # shouldn't restrict
call file.flush allow                   # they are free to use
call file.next allow                    # free to use as well...
call file.read allow                    # allow read
call file.readline allow                # shouldn't restrict
call file.readlines allow               # shouldn't restrict
call file.seek allow                    # seek doesn't restrict
call file.write allow                   # shouldn't restrict (open restricts)
call file.writelines allow              # shouldn't restrict (open restricts)
call sleep allow                        # harmless
call settimer allow                     # we can't really do anything smart
call canceltimer allow                  # should be okay
call exitall allow                      # should be harmless 

call log.write allow
call log.writelines allow
call getmyip allow                      # They can get the external IP address
call listdir allow                      # They can list the files they created
call removefile allow                   # They can remove the files they create
call randomfloat allow                  # can get random numbers
call getruntime allow                   # can get the elapsed time
call getlock allow                      # can get a mutex
"""





def make_vessel(vesselname, pubkey, resourcetemplate, resourceargs):
  retdict = {'userkeys':[], 'ownerkey':pubkey, 'oldmetadata':None, 'stopfilename':vesselname+'.stop', 'logfilename':vesselname+'.log', 'statusfilename':vesselname+'.status', 'resourcefilename':'resource.'+vesselname, 'advertise':True, 'ownerinformation':'', 'status':'Fresh'}

  try:
    WindowsError

  except NameError: # not on windows...
    # make the vessel dirs...
    try:
      os.mkdir(vesselname)
    except OSError,e:
      if e[0] == 17:
        # directory exists
        pass
      else:
        raise

  else: # on Windows...

    # make the vessel dirs...
    try:
      os.mkdir(vesselname)
    except (OSError,WindowsError),e:
      if e[0] == 17 or e[0] == 183:
        # directory exists
        pass
      else:
        raise


  #### write the vessel's resource file...
  outfo = open(retdict['resourcefilename'],"w")
  # write the args into the resource data template
  outfo.write(resourcetemplate % resourceargs)
  outfo.close()
  
  return retdict



# lots of little things need to be initialized...   
def initialize_state():

  # first, let's clean up any existing directory data...
  for vesseldirectoryname in glob.glob('v[0-9]*'):
    if os.path.isdir(vesseldirectoryname):
      print 'Removing:',vesseldirectoryname
      shutil.rmtree(vesseldirectoryname)

  # initialize my configuration file.   This involves a few variables:
  #    pollfrequency --  the amount of time to sleep after a check when "busy
  #                      waiting".   This trades CPU load for responsiveness.
  #    ports         --  the ports the node manager could listen on.
  #    publickey     --  the public key used to identify the node...
  #    privatekey    --  the corresponding private key for the node...
  configuration = {}

  configuration['pollfrequency'] = 1.0

  # NOTE: I chose these randomly (they will be uniform across all NMs)...   
  # Was this wise?
  configuration['ports'] = [1224, 2888, 9625, 10348, 39303, 48126, 52862, 57344, 64310]

  print "Generating key..."
  keys = rsa_gen_pubpriv_keys(100)
  configuration['publickey'] = keys[0]
  configuration['privatekey'] = keys[1]
  configuration['service_vessel'] = 'v2'

  print "Writing config file..."
  # write the config file...
  persist.commit_object(configuration,"nodeman.cfg")

  # write the offcut file...
  outfo = open("resources.offcut","w")
  outfo.write(offcutresourcedata)
  outfo.close()

#  vessel1 = make_vessel('v1',controllerpubkey,bigresourcedata, []) 
  vessel1 = make_vessel('v1',controllerpubkey,smallresourcedata, ('12345','12346', '12347','12348','12345','12346','12347','12348')) 
  vessel2 = make_vessel('v2',justinpubkey,smallresourcedata, ('20000','20001', '20002','20003','20000','20001','20002','20003')) 
  vessel3 = make_vessel('v3',ivanpubkey,smallresourcedata, ('30000','30001', '30002','30003','30000','30001','30002','30003')) 
  vessel4 = make_vessel('v4',andreaspubkey,smallresourcedata, ('21000','21001', '21002','21003','21000','21001','21002','21003')) 
  vessel5 = make_vessel('v5',brentpubkey,smallresourcedata, ('22000','22001', '22002','22003','22000','22001','22002','22003')) 
  vessel6 = make_vessel('v6',carterpubkey,smallresourcedata, ('23000','23001', '23002','23003','23000','23001','23002','23003')) 
  vessel7 = make_vessel('v7',armonpubkey,smallresourcedata, ('24000','24001', '24002','24003','24000','24001','24002','24003')) 
  vessel8 = make_vessel('v8',cosminpubkey,smallresourcedata, ('25000','25001', '25002','25003','25000','25001','25002','25003')) 
  vessel9 = make_vessel('v9',kimbrlpubkey,smallresourcedata, ('26000','26001', '26002','26003','26000','26001','26002','26003')) 
  vessel10 = make_vessel('v10',whitakerpubkey,smallresourcedata, ('27000','27001', '27002','27003','27000','27001','27002','27003')) 
  

  vesseldict = {'v1':vessel1, 'v2':vessel2, 'v3':vessel3, 'v4':vessel4, 'v5':vessel5, 'v6':vessel6, 'v7':vessel7, 'v8':vessel8, 'v9':vessel9, 'v10':vessel10}

  print "Writing vessel dictionary..."
  # write out the vessel dictionary...
  persist.commit_object(vesseldict,"vesseldict")










if __name__ == '__main__':
  initialize_state() 
