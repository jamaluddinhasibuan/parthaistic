import streamlit as st
import pandas as pd
import random
import time
from io import StringIO

# Konfigurasi Halaman
st.set_page_config(
    page_title="Parthaistic - Dashboard Rekomendasi Calon Klien",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS Kustom yang sederhana dan profesional
st.markdown("""
<style>
    /* Reset dan base styles */
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    /* Font yang bersih */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .stApp {
        font-family: 'Inter', sans-serif;
    }
    
    /* Header utama */
    .main-header {
        font-size: 2.5rem;
        color: #1e293b;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: 700;
        padding: 20px 0;
        border-bottom: 1px solid #e2e8f0;
    }
    
    .sub-header {
        font-size: 1.2rem;
        color: #64748b;
        text-align: center;
        margin-bottom: 2.5rem;
        font-weight: 400;
    }
    
    /* Hero Section yang bersih */
    .hero-section {
        background: #f8fafc;
        border-radius: 12px;
        padding: 3rem 2rem;
        margin: 2rem 0;
        text-align: center;
        border: 1px solid #e2e8f0;
    }
    
    .hero-title {
        font-size: 2rem;
        color: #1e293b;
        margin-bottom: 1rem;
        font-weight: 600;
    }
    
    .hero-description {
        color: #64748b;
        font-size: 1.1rem;
        max-width: 800px;
        margin: 0 auto;
        line-height: 1.6;
    }
    
    /* Stats Card */
    .stats-card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        border: 1px solid #e2e8f0;
        text-align: center;
        transition: all 0.2s ease;
    }
    
    .stats-card:hover {
        border-color: #3b82f6;
    }
    
    .stats-number {
        font-size: 2.2rem;
        font-weight: 700;
        color: #3b82f6;
        margin-bottom: 8px;
    }
    
    .stats-label {
        font-size: 0.95rem;
        color: #475569;
        font-weight: 500;
    }
    
    /* Recommendation Card */
    .recommendation-card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        border: 1px solid #e2e8f0;
        transition: all 0.2s ease;
    }
    
    .recommendation-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        border-color: #3b82f6;
    }
    
    .username-badge {
        background: #eff6ff;
        color: #1d4ed8;
        padding: 0.4rem 1rem;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: 600;
        display: inline-block;
        margin-bottom: 1rem;
        border: 1px solid #dbeafe;
    }
    
    /* Search Button */
    .search-button {
        background: #3b82f6;
        color: white;
        border: none;
        padding: 0.9rem 2rem;
        border-radius: 8px;
        font-size: 1rem;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.2s ease;
        display: inline-block;
        margin: 1rem 0;
    }
    
    .search-button:hover {
        background: #2563eb;
        transform: translateY(-1px);
    }
    
    /* Loading State */
    .loading-container {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        gap: 20px;
        margin: 3rem 0;
        padding: 3rem;
        background: #f8fafc;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
    }
    
    .loading-title {
        font-size: 1.5rem;
        color: #1e293b;
        font-weight: 600;
        text-align: center;
    }
    
    .loading-subtitle {
        font-size: 1rem;
        color: #64748b;
        text-align: center;
    }
    
    /* Progress bar sederhana */
    .progress-bar {
        width: 100%;
        height: 6px;
        background: #e2e8f0;
        border-radius: 3px;
        overflow: hidden;
        margin-top: 20px;
        max-width: 400px;
    }
    
    .progress-fill {
        height: 100%;
        background: #3b82f6;
        width: 0%;
        border-radius: 3px;
    }
    
    /* Result section */
    .result-count {
        background: #10b981;
        color: white;
        padding: 0.7rem 1.5rem;
        border-radius: 20px;
        font-size: 1rem;
        font-weight: 600;
        display: inline-block;
        margin-bottom: 1.5rem;
    }
    
    /* Instagram link */
    .instagram-link {
        color: #e4405f;
        text-decoration: none;
        font-weight: 500;
        display: inline-flex;
        align-items: center;
        gap: 5px;
        margin-top: 0.5rem;
        padding: 0.4rem 0.8rem;
        background: #fff1f2;
        border-radius: 6px;
        border: 1px solid #fecdd3;
    }
    
    .instagram-link:hover {
        background: #ffe4e6;
        text-decoration: underline;
    }
    
    /* Tips box */
    .tips-box {
        background: #f0fdf4;
        border: 1px solid #bbf7d0;
        border-radius: 10px;
        padding: 1.5rem;
        margin-top: 2rem;
    }
    
    .tips-title {
        color: #16a34a;
        font-size: 1.1rem;
        font-weight: 600;
        margin-bottom: 0.8rem;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    /* Responsive adjustments */
    @media (max-width: 768px) {
        .main-header {
            font-size: 2rem;
        }
        
        .hero-section {
            padding: 2rem 1rem;
        }
        
        .hero-title {
            font-size: 1.5rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# Data Instagram lengkap (sama seperti sebelumnya)
INSTAGRAM_DATA = """Link Instagram,Username
https://www.instagram.com/mimi.peri/,mimi.peri
https://www.instagram.com/riomotret/,riomotret
https://www.instagram.com/hanaabas92/,hanaabas92
https://www.instagram.com/kiesha.alvaro/,kiesha.alvaro
https://www.instagram.com/its_lauramoane2/,its_lauramoane2
https://www.instagram.com/elleonora.rika/,elleonora.rika
https://www.instagram.com/aldosinarta/,aldosinarta
https://www.instagram.com/salshabillaadr/,salshabillaadr
https://www.instagram.com/fransiscawdya/,fransiscawdya
https://www.instagram.com/garemcapsoang/,garemcapsoang
https://www.instagram.com/adisurantha/,adisurantha
https://www.instagram.com/zidan.trisnanto/,zidan.trisnanto
https://www.instagram.com/seeforcare/,seeforcare
https://www.instagram.com/snap.nuel/,snap.nuel
https://www.instagram.com/liyanzef/,liyanzef
https://www.instagram.com/claygribble/,claygribble
https://www.instagram.com/converse_id/,converse_id
https://www.instagram.com/deevadep_/,deevadep_
https://www.instagram.com/nicole_rossi_/,nicole_rossi_
https://www.instagram.com/zayyansakha/,zayyansakha
https://www.instagram.com/sinetron.sctv/,sinetron.sctv
https://www.instagram.com/real.hanummegaa/,real.hanummegaa
https://www.instagram.com/saaihalilintar/,saaihalilintar
https://www.instagram.com/opa.jahja/,opa.jahja
https://www.instagram.com/r_marrwt/,r_marrwt
https://www.instagram.com/samudra.taylor/,samudra.taylor
https://www.instagram.com/na1ma._/,na1ma._
https://www.instagram.com/shint_ta/,shint_ta
https://www.instagram.com/arellaraina/,arellaraina
https://www.instagram.com/yasminnapper/,yasminnapper
https://www.instagram.com/randymartinnn/,randymartinnn
https://www.instagram.com/biandanadia/,biandanadia
https://www.instagram.com/danjyohiyoji/,danjyohiyoji
https://www.instagram.com/aisyahaqilahh/,aisyahaqilahh
https://www.instagram.com/naymirdad/,naymirdad
https://www.instagram.com/yndlaurens/,yndlaurens
https://www.instagram.com/keisyalevronka/,keisyalevronka
https://www.instagram.com/andi_nopianto00/,andi_nopianto00
https://www.instagram.com/dindakirana.s/,dindakirana.s
https://www.instagram.com/jeartofa/,jeartofa
https://www.instagram.com/nayo_chio/,nayo_chio
https://www.instagram.com/prencong_jakarta/,prencong_jakarta
https://www.instagram.com/fariz_irawan/,fariz_irawan
https://www.instagram.com/gde_karya69/,gde_karya69
https://www.instagram.com/indridimassinggih/,indridimassinggih
https://www.instagram.com/intan_ahmad/,intan_ahmad
https://www.instagram.com/mulanisanjay/,mulanisanjay
https://www.instagram.com/artistinc.id/,artistinc.id
https://www.instagram.com/santa_paris_jakarta/,santa_paris_jakarta
https://www.instagram.com/av9zs/,av9zs
https://www.instagram.com/stephaniepoetri/,stephaniepoetri
https://www.instagram.com/wildawidy/,wildawidy
https://www.instagram.com/inpower.id/,inpower.id
https://www.instagram.com/farell.akbar11/,farell.akbar11
https://www.instagram.com/saridano/,saridano
https://www.instagram.com/zulfasyamlan/,zulfasyamlan
https://www.instagram.com/rinijuarsa/,rinijuarsa
https://www.instagram.com/chechewe_22/,chechewe_22
https://www.instagram.com/rgy_f/,rgy_f
https://www.instagram.com/fanadnt/,fanadnt
https://www.instagram.com/gadismagz/,gadismagz
https://www.instagram.com/latte_jkt/,latte_jkt
https://www.instagram.com/vita_ngangas/,vita_ngangas
https://www.instagram.com/delanodaniel/,delanodaniel
https://www.instagram.com/babby_key_nahd/,babby_key_nahd
https://www.instagram.com/cantik_shalzabillah/,cantik_shalzabillah
https://www.instagram.com/m.husnanhabib/,m.husnanhabib
https://www.instagram.com/pm_photoworks/,pm_photoworks
https://www.instagram.com/nadafikalopurba/,nadafikalopurba
https://www.instagram.com/zahralarafi/,zahralarafi
https://www.instagram.com/patriciagouw/,patriciagouw
https://www.instagram.com/faul.gayo19/,faul.gayo19
https://www.instagram.com/aliffarrasya21/,aliffarrasya21
https://www.instagram.com/gabriellacawley2/,gabriellacawley2
https://www.instagram.com/queenvalishaa/,queenvalishaa
https://www.instagram.com/ramzialmuzaki_/,ramzialmuzaki_
https://www.instagram.com/amesharianty_/,amesharianty_
https://www.instagram.com/winstongomez/,winstongomez
https://www.instagram.com/mumtaz.raffy/,mumtaz.raffy
https://www.instagram.com/wulanpurwanti89/,wulanpurwanti89
https://www.instagram.com/yourminbite/,yourminbite
https://www.instagram.com/audymaulidyna/,audymaulidyna
https://www.instagram.com/byputy/,byputy
https://www.instagram.com/jessavanathan/,jessavanathan
https://www.instagram.com/arasha.skater/,arasha.skater
https://www.instagram.com/viansfn/,viansfn
https://www.instagram.com/zzieie/,zzieie
https://www.instagram.com/ktriana10/,ktriana10
https://www.instagram.com/nevytaania/,nevytaania
https://www.instagram.com/ryanpitna/,ryanpitna
https://www.instagram.com/syanaalha/,syanaalha
https://www.instagram.com/asha.assuncao/,asha.assuncao
https://www.instagram.com/gemavya__/,gemavya__
https://www.instagram.com/ridho.firmansyahhh/,ridho.firmansyahhh
https://www.instagram.com/novriinayati/,novriinayati
https://www.instagram.com/bremagintings/,bremagintings
https://www.instagram.com/citrazein/,citrazein
https://www.instagram.com/radhsvi/,radhsvi
https://www.instagram.com/patricia_angelie_tan/,patricia_angelie_tan
https://www.instagram.com/davidsuwarto/,davidsuwarto
https://www.instagram.com/endri_sano/,endri_sano
https://www.instagram.com/bapack2pesonk/,bapack2pesonk
https://www.instagram.com/gloowandbe/,gloowandbe
https://www.instagram.com/salwastwti/,salwastwti
https://www.instagram.com/queency.alycia/,queency.alycia
https://www.instagram.com/ersa_puspa/,ersa_puspa
https://www.instagram.com/isabel.azhari/,isabel.azhari
https://www.instagram.com/aryamohan7/,aryamohan7
https://www.instagram.com/almer_vicko/,almer_vicko
https://www.instagram.com/azizi.althaf/,azizi.althaf
https://www.instagram.com/dndabrlyn09/,dndabrlyn09
https://www.instagram.com/_dimasputt/,_dimasputt
https://www.instagram.com/allyciasyllm/,allyciasyllm
https://www.instagram.com/naldyf/,naldyf
https://www.instagram.com/aimanameeraa/,aimanameeraa
https://www.instagram.com/mikha_hernan/,mikha_hernan
https://www.instagram.com/aya.mazayaa/,aya.mazayaa
https://www.instagram.com/aliefindr/,aliefindr
https://www.instagram.com/papabearwisnu/,papabearwisnu
https://www.instagram.com/dimas.agsa/,dimas.agsa
https://www.instagram.com/jrocks.official/,jrocks.official
https://www.instagram.com/ranieroo/,ranieroo
https://www.instagram.com/reginafransissca/,reginafransissca
https://www.instagram.com/gabrihella_/,gabrihella_
https://www.instagram.com/ramlihursan/,ramlihursan
https://www.instagram.com/azzurabisyir/,azzurabisyir
https://www.instagram.com/sandro_karamoy/,sandro_karamoy
https://www.instagram.com/paca.sweetandsavory/,paca.sweetandsavory
https://www.instagram.com/shennyra/,shennyra
https://www.instagram.com/juliastv2015/,juliastv2015
https://www.instagram.com/mrizkyra_/,mrizkyra_
https://www.instagram.com/eddy_mm/,eddy_mm
https://www.instagram.com/andreriva77/,andreriva77
https://www.instagram.com/anggaharyono_/,anggaharyono_
https://www.instagram.com/suciasabrina/,suciasabrina
https://www.instagram.com/mia_kalipancur/,mia_kalipancur
https://www.instagram.com/sutisnaagus523/,sutisnaagus523
https://www.instagram.com/bindusamtani/,bindusamtani
https://www.instagram.com/razanzu/,razanzu
https://www.instagram.com/raniabisyir/,raniabisyir
https://www.instagram.com/masnanda___/,masnanda___
https://www.instagram.com/windyhartanto/,windyhartanto
https://www.instagram.com/kaktyann/,kaktyann
https://www.instagram.com/mikhayla_rezky/,mikhayla_rezky
https://www.instagram.com/sitiwiryani/,sitiwiryani
https://www.instagram.com/zaza_seca/,zaza_seca
https://www.instagram.com/m_ara1950/,m_ara1950
https://www.instagram.com/karissa_meme/,karissa_meme
https://www.instagram.com/bintangsci/,bintangsci
https://www.instagram.com/michellechrlt_/,michellechrlt_
https://www.instagram.com/raniasalsabilaazzahra/,raniasalsabilaazzahra
https://www.instagram.com/hanzhp/,hanzhp
https://www.instagram.com/azaclothing.co/,azaclothing.co
https://www.instagram.com/zavieraa.co/,zavieraa.co
https://www.instagram.com/shahnazbsyr/,shahnazbsyr
https://www.instagram.com/izzatassegaf/,izzatassegaf
https://www.instagram.com/meytariarosalina/,meytariarosalina
https://www.instagram.com/jadenbahtera/,jadenbahtera
https://www.instagram.com/antokaunang/,antokaunang
https://www.instagram.com/yogidarmawansyah96/,yogidarmawansyah96
https://www.instagram.com/magejibril/,magejibril
https://www.instagram.com/bazaarin.id/,bazaarin.id
https://www.instagram.com/fattsyach/,fattsyach
https://www.instagram.com/vaniapriscilla.real/,vaniapriscilla.real
https://www.instagram.com/tennyaininnisa/,tennyaininnisa
https://www.instagram.com/ammar.mahija.razzaq/,ammar.mahija.razzaq
https://www.instagram.com/alejandro.cool/,alejandro.cool
https://www.instagram.com/xavieraalanna/,xavieraalanna
https://www.instagram.com/sintadella.real/,sintadella.real
https://www.instagram.com/alejandromarianoo/,alejandromarianoo
https://www.instagram.com/nenarosier/,nenarosier
https://www.instagram.com/dickymakeup/,dickymakeup
https://www.instagram.com/wasrinita/,wasrinita
https://www.instagram.com/ikrarsr/,ikrarsr
https://www.instagram.com/gitapanhar/,gitapanhar
https://www.instagram.com/melodyamanda_25/,melodyamanda_25
https://www.instagram.com/gwella.id/,gwella.id
https://www.instagram.com/auleenn/,auleenn
https://www.instagram.com/elissa_haddadxx/,elissa_haddadxx
https://www.instagram.com/jokonugroho2115/,jokonugroho2115
https://www.instagram.com/jihanrnt1/,jihanrnt1
https://www.instagram.com/asmaragt/,asmaragt
https://www.instagram.com/matthewkenevan/,matthewkenevan
https://www.instagram.com/dayangida_instyle/,dayangida_instyle
https://www.instagram.com/dafauguciano/,dafauguciano
https://www.instagram.com/hilgadoui/,hilgadoui
https://www.instagram.com/keeamacleod/,keeamacleod
https://www.instagram.com/aqeeverss_1406/,aqeeverss_1406
https://www.instagram.com/andilagii/,andilagii
https://www.instagram.com/alanamusicofficial/,alanamusicofficial
https://www.instagram.com/agustia_nursiti/,agustia_nursiti
https://www.instagram.com/zafiraadelia/,zafiraadelia
https://www.instagram.com/aldyqullriz/,aldyqullriz
https://www.instagram.com/arumakhadijah/,arumakhadijah
https://www.instagram.com/firmannnf/,firmannnf
https://www.instagram.com/nadya.yusuf/,nadya.yusuf
https://www.instagram.com/itsichey/,itsichey
https://www.instagram.com/houseofdimassinggih/,houseofdimassinggih
https://www.instagram.com/ammarmahijarazzaq/,ammarmahijarazzaq
https://www.instagram.com/neysachandria/,neysachandria
https://www.instagram.com/xxayukar_/,xxayukar_
https://www.instagram.com/dinda.ghaniaa/,dinda.ghaniaa
https://www.instagram.com/gitapilar/,gitapilar
https://www.instagram.com/jojoohalim/,jojoohalim
https://www.instagram.com/felix.hasibuan/,felix.hasibuan
https://www.instagram.com/audreyralinka/,audreyralinka
https://www.instagram.com/fauzanharish/,fauzanharish
https://www.instagram.com/therealfidiany/,therealfidiany
https://www.instagram.com/asyaroh.98/,asyaroh.98
https://www.instagram.com/evifebriyantii/,evifebriyantii
https://www.instagram.com/faruxruxli/,faruxruxli
https://www.instagram.com/srnentertainment_official/,srnentertainment_official
https://www.instagram.com/megarymnd/,megarymnd
https://www.instagram.com/edwinstevenl/,edwinstevenl
https://www.instagram.com/andyw24_/,andyw24_
https://www.instagram.com/idahaddad/,idahaddad
https://www.instagram.com/valdyp_s7ven/,valdyp_s7ven
https://www.instagram.com/blackantgamestation/,blackantgamestation
https://www.instagram.com/ratuurafa/,ratuurafa
https://www.instagram.com/braynlim/,braynlim
https://www.instagram.com/polinviona/,polinviona
https://www.instagram.com/rbananto/,rbananto
https://www.instagram.com/aridanik76/,aridanik76
https://www.instagram.com/riskaftriaa_/,riskaftriaa_
https://www.instagram.com/syifakamaliaa_/,syifakamaliaa_
https://www.instagram.com/drina07/,drina07
https://www.instagram.com/alunarizk/,alunarizk
https://www.instagram.com/reyromy98/,reyromy98
https://www.instagram.com/putrigitaaaa___/,putrigitaaaa___
https://www.instagram.com/raisamariee_/,raisamariee_
https://www.instagram.com/citraa1121/,citraa1121
https://www.instagram.com/aa_ahmad/,aa_ahmad
https://www.instagram.com/khosyi_aidillana/,khosyi_aidillana
https://www.instagram.com/nopekkk/,nopekkk
https://www.instagram.com/androtrinanda/,androtrinanda
https://www.instagram.com/nanang_khan/,nanang_khan
https://www.instagram.com/yusufyudo/,yusufyudo
https://www.instagram.com/dapoermaemun/,dapoermaemun
https://www.instagram.com/candra_ngan/,candra_ngan
https://www.instagram.com/avhiedop/,avhiedop
https://www.instagram.com/silvansaputra/,silvansaputra
https://www.instagram.com/jameshartono/,jameshartono
https://www.instagram.com/jisunkang_/,jisunkang_
https://www.instagram.com/richelprabarini/,richelprabarini
https://www.instagram.com/youmnald/,youmnald
https://www.instagram.com/angga_sastro/,angga_sastro
https://www.instagram.com/harry.vghn/,harry.vghn
https://www.instagram.com/lovelysilvia_/,lovelysilvia_
https://www.instagram.com/rhyawilko/,rhyawilko
https://www.instagram.com/f.talithaa/,f.talithaa
https://www.instagram.com/taufik.t7/,taufik.t7
https://www.instagram.com/ditodarmawan__/,ditodarmawan__
https://www.instagram.com/nduthspears/,nduthspears
https://www.instagram.com/revimasyitaaa/,revimasyitaaa
https://www.instagram.com/aqueneazizdjorghi/,aqueneazizdjorghi
https://www.instagram.com/ichsanrindengan/,ichsanrindengan
https://www.instagram.com/susan_rossi_/,susan_rossi_
https://www.instagram.com/hayu_pangastuti/,hayu_pangastuti
https://www.instagram.com/ammarsyahdi/,ammarsyahdi
https://www.instagram.com/mickomentari/,mickomentari
https://www.instagram.com/bertram_beryl/,bertram_beryl
https://www.instagram.com/sanyandsusanti/,sanyandsusanti
https://www.instagram.com/kickmanagement.id/,kickmanagement.id
https://www.instagram.com/oneshotonekill.camera/,oneshotonekill.camera
https://www.instagram.com/sinemart_ph/,sinemart_ph
https://www.instagram.com/falconpictures_/,falconpictures_
https://www.instagram.com/rassyahidayahreal/,rassyahidayahreal
https://www.instagram.com/andrewxbarrett/,andrewxbarrett
https://www.instagram.com/syaradivaazima/,syaradivaazima
https://www.instagram.com/deankhalil/,deankhalil
https://www.instagram.com/denyssimon/,denyssimon
https://www.instagram.com/adriankhalif/,adriankhalif
https://www.instagram.com/_william_xu/,_william_xu
https://www.instagram.com/siscamagdalena_/,siscamagdalena_
https://www.instagram.com/diandraich/,diandraich
https://www.instagram.com/anggayoya/,anggayoya
https://www.instagram.com/putrirahay/,putrirahay
https://www.instagram.com/pratiwinurel/,pratiwinurel
https://www.instagram.com/sulaimanbsyr/,sulaimanbsyr
https://www.instagram.com/sastra.silalahii/,sastra.silalahii
https://www.instagram.com/rahmaniarrusnan/,rahmaniarrusnan
https://www.instagram.com/nuradatau/,nuradatau
https://www.instagram.com/narulita_maharani/,narulita_maharani
https://www.instagram.com/tristan_alif_naufal/,tristan_alif_naufal
https://www.instagram.com/mrs.rani_tdj/,mrs.rani_tdj
https://www.instagram.com/yuriwa_0811/,yuriwa_0811
https://www.instagram.com/baselxendra/,baselxendra
https://www.instagram.com/shalby08/,shalby08
https://www.instagram.com/tasyacarlla27/,tasyacarlla27
https://www.instagram.com/rendiputrasetiawan/,rendiputrasetiawan
https://www.instagram.com/ricky_zakno/,ricky_zakno
https://www.instagram.com/iduradewijaya/,iduradewijaya
https://www.instagram.com/dewisaputra83/,dewisaputra83
https://www.instagram.com/ziziezidane/,ziziezidane
https://www.instagram.com/naufala2/,naufala2
https://www.instagram.com/meliza_hutasoit/,meliza_hutasoit
https://www.instagram.com/alfaris_1818/,alfaris_1818
https://www.instagram.com/official.aqeevers/,official.aqeevers
https://www.instagram.com/antonjrocks.kelces/,antonjrocks.kelces
https://www.instagram.com/sabrinabisyirr/,sabrinabisyirr
https://www.instagram.com/ghinarai/,ghinarai
https://www.instagram.com/xandrahardian/,xandrahardian
https://www.instagram.com/upie_samsimar/,upie_samsimar
https://www.instagram.com/putrasiregarr17/,putrasiregarr17
https://www.instagram.com/yoongimenez/,yoongimenez
https://www.instagram.com/prialangga_/,prialangga_
https://www.instagram.com/bimasenaprisai_/,bimasenaprisai_
https://www.instagram.com/imelda_lubis9/,imelda_lubis9
https://www.instagram.com/ney_neo/,ney_neo
https://www.instagram.com/ranggayusuf/,ranggayusuf
https://www.instagram.com/sheilakusnadi_/,sheilakusnadi_
https://www.instagram.com/willyjn15/,willyjn15
https://www.instagram.com/kanmogroup.fashion/,kanmogroup.fashion
https://www.instagram.com/sheemar_rahman/,sheemar_rahman
https://www.instagram.com/rafidahalatas/,rafidahalatas
https://www.instagram.com/adli_umar/,adli_umar
https://www.instagram.com/dude2harlino/,dude2harlino
https://www.instagram.com/nabilazaviraa_/,nabilazaviraa_
https://www.instagram.com/flaviozavieraa/,flaviozavieraa
https://www.instagram.com/azxtha/,azxtha
https://www.instagram.com/washeudee/,washeudee
https://www.instagram.com/cantikaaputrikirana/,cantikaaputrikirana
https://www.instagram.com/danieltito13/,danieltito13
https://www.instagram.com/bnhimawan/,bnhimawan
https://www.instagram.com/tha2_nez/,tha2_nez
https://www.instagram.com/diansidik_/,diansidik_
https://www.instagram.com/chairul.giano/,chairul.giano
https://www.instagram.com/irien_heriyanto/,irien_heriyanto
https://www.instagram.com/ratusfy_/,ratusfy_
https://www.instagram.com/sabrinasoetomo/,sabrinasoetomo
https://www.instagram.com/rezadpy/,rezadpy
https://www.instagram.com/diva.mn/,diva.mn
https://www.instagram.com/umamap2/,umamap2
https://www.instagram.com/moedjenan/,moedjenan
https://www.instagram.com/oki.hartanto/,oki.hartanto
https://www.instagram.com/zolada_mum/,zolada_mum
https://www.instagram.com/madeardanaofficial/,madeardanaofficial
https://www.instagram.com/kimmyyyyy.kim/,kimmyyyyy.kim
https://www.instagram.com/delon_mercy_/,delon_mercy_
https://www.instagram.com/mike.lucock/,mike.lucock
https://www.instagram.com/yudetraaj/,yudetraaj
https://www.instagram.com/shendykarunia_/,shendykarunia_
https://www.instagram.com/zheyamada_/,zheyamada_
https://www.instagram.com/tamarasyarief/,tamarasyarief
https://www.instagram.com/hauralathifarz/,hauralathifarz
https://www.instagram.com/andrewchriz/,andrewchriz
https://www.instagram.com/nonaeurny/,nonaeurny
https://www.instagram.com/diraamel/,diraamel
https://www.instagram.com/roymagny/,roymagny
https://www.instagram.com/ikkedspt/,ikkedspt
https://www.instagram.com/lindasaibi/,lindasaibi
https://www.instagram.com/nadiaraysa/,nadiaraysa
https://www.instagram.com/devhianrhasan/,devhianrhasan
https://www.instagram.com/chelseaconcheta/,chelseaconcheta
https://www.instagram.com/albielatief/,albielatief
https://www.instagram.com/kartikaputr/,kartikaputr
https://www.instagram.com/wetvindonesia/,wetvindonesia
https://www.instagram.com/ibamadr/,ibamadr
https://www.instagram.com/riizkkaaay/,riizkkaaay
https://www.instagram.com/kimora_razi/,kimora_razi
https://www.instagram.com/ebasheba/,ebasheba
https://www.instagram.com/sriwadebarrett/,sriwadebarrett
https://www.instagram.com/nadialaydrus/,nadialaydrus
https://www.instagram.com/dyah_gayatri/,dyah_gayatri
https://www.instagram.com/shofia_shireen/,shofia_shireen
https://www.instagram.com/mayangwulansantoso/,mayangwulansantoso
https://www.instagram.com/ms.pipit_puspitawardhaniadjie/,ms.pipit_puspitawardhaniadjie
https://www.instagram.com/_darimatakemata/,_darimatakemata
https://www.instagram.com/jscamandy/,jscamandy
https://www.instagram.com/qheylazv/,qheylazv
https://www.instagram.com/nadhifbasalamah/,nadhifbasalamah
https://www.instagram.com/rhiofaldo/,rhiofaldo
https://www.instagram.com/nafisahnjlaa/,nafisahnjlaa
https://www.instagram.com/baetzmanagement/,baetzmanagement
https://www.instagram.com/zorayaudri/,zorayaudri
https://www.instagram.com/deniirawan1981/,deniirawan1981
https://www.instagram.com/rennov3011/,rennov3011
https://www.instagram.com/ebel_cobra/,ebel_cobra
https://www.instagram.com/falconmusic/,falconmusic
https://www.instagram.com/dienz_36/,dienz_36
https://www.instagram.com/lesleyvs/,lesleyvs
https://www.instagram.com/leciel.design/,leciel.design
https://www.instagram.com/alineefziah/,alineefziah
https://www.instagram.com/haedy_dot/,haedy_dot
https://www.instagram.com/joe_chandra28/,joe_chandra28
https://www.instagram.com/nowayisthataki/,nowayisthataki
https://www.instagram.com/angelinacortizo/,angelinacortizo
https://www.instagram.com/naylayuu/,naylayuu
https://www.instagram.com/ichanvirgo_new/,ichanvirgo_new
https://www.instagram.com/yudhahehehe/,yudhahehehe
https://www.instagram.com/diniajah12/,diniajah12
https://www.instagram.com/jay82sandy/,jay82sandy
https://www.instagram.com/williamroberts08/,williamroberts08
https://www.instagram.com/almanuraaa/,almanuraaa
https://www.instagram.com/lutfihasby/,lutfihasby
https://www.instagram.com/mryogiepratama/,mryogiepratama
https://www.instagram.com/harunempenk/,harunempenk
https://www.instagram.com/reza.ekas/,reza.ekas
https://www.instagram.com/rurypadwa/,rurypadwa
https://www.instagram.com/yehuda.gilbert/,yehuda.gilbert
https://www.instagram.com/dindaaaaa.17/,dindaaaaa.17
https://www.instagram.com/kiaramckenna/,kiaramckenna
https://www.instagram.com/feliciablancomua/,feliciablancomua
https://www.instagram.com/kamilrff/,kamilrff
https://www.instagram.com/arry_dharyanto/,arry_dharyanto
https://www.instagram.com/andikapangestu19/,andikapangestu19
https://www.instagram.com/viecawley/,viecawley
https://www.instagram.com/kangadetalco/,kangadetalco
https://www.instagram.com/jinan.safaa/,jinan.safaa
https://www.instagram.com/svastiari/,svastiari
https://www.instagram.com/kenyolw/,kenyolw
https://www.instagram.com/ajeng_faradita/,ajeng_faradita
https://www.instagram.com/lintangamel/,lintangamel
https://www.instagram.com/medigerdiandi/,medigerdiandi
https://www.instagram.com/teukuanwar/,teukuanwar
https://www.instagram.com/keanurne/,keanurne
https://www.instagram.com/brideseries/,brideseries
https://www.instagram.com/riz.basey/,riz.basey
https://www.instagram.com/hiitstheoo/,hiitstheoo
https://www.instagram.com/un1ty_official/,un1ty_official
https://www.instagram.com/ariksyach/,ariksyach
https://www.instagram.com/ronny_irawan/,ronny_irawan
https://www.instagram.com/hairbyranggayusuf/,hairbyranggayusuf
https://www.instagram.com/bungafathia06/,bungafathia06
https://www.instagram.com/silvyprajogo/,silvyprajogo
https://www.instagram.com/bunda.latinas/,bunda.latinas
https://www.instagram.com/thecataracs/,thecataracs
https://www.instagram.com/bravyson.vconk/,bravyson.vconk
https://www.instagram.com/acidlineave/,acidlineave
https://www.instagram.com/kaay.raw/,kaay.raw
https://www.instagram.com/richardricardoo/,richardricardoo
https://www.instagram.com/titipdongkak_reborn/,titipdongkak_reborn
https://www.instagram.com/okintph/,okintph
https://www.instagram.com/snap.nuel/,snap.nuel
https://www.instagram.com/adlianesa/,adlianesa
https://www.instagram.com/nickyromero/,nickyromero
https://www.instagram.com/greg11n/,greg11n
https://www.instagram.com/revelation.stage/,revelation.stage
https://www.instagram.com/wowshack/,wowshack
https://www.instagram.com/aldosinarta/,aldosinarta
https://www.instagram.com/warkop.rinjani/,warkop.rinjani
https://www.instagram.com/the.atami/,the.atami
https://www.instagram.com/seiru0711/,seiru0711
https://www.instagram.com/audien/,audien
https://www.instagram.com/yuliabaltschun/,yuliabaltschun
https://www.instagram.com/noizemafia/,noizemafia
https://www.instagram.com/adindapuri/,adindapuri
https://www.instagram.com/lunpharrin/,lunpharrin
https://www.instagram.com/tchindaeliza/,tchindaeliza
https://www.instagram.com/vercit/,vercit
https://www.instagram.com/nareend/,nareend
https://www.instagram.com/yoshehairdo/,yoshehairdo
https://www.instagram.com/sabrinasameh/,sabrinasameh
https://www.instagram.com/bossybabe.id/,bossybabe.id
https://www.instagram.com/prettycia.official/,prettycia.official
https://www.instagram.com/kodkushi/,kodkushi
https://www.instagram.com/alyafrcn/,alyafrcn
https://www.instagram.com/thelist.bali/,thelist.bali
https://www.instagram.com/maria.ishida/,maria.ishida
https://www.instagram.com/kshmr/,kshmr
https://www.instagram.com/zai_cafe/,zai_cafe
https://www.instagram.com/__star101__/,__star101__
https://www.instagram.com/supirdieropa/,supirdieropa
https://www.instagram.com/christamcqueen.mua/,christamcqueen.mua
https://www.instagram.com/riskylaskyyy/,riskylaskyyy
https://www.instagram.com/ridho.ghonim/,ridho.ghonim
https://www.instagram.com/irliewijanarko/,irliewijanarko
https://www.instagram.com/vilotisss/,vilotisss
https://www.instagram.com/iniadzwaaurell/,iniadzwaaurell
https://www.instagram.com/eby.adinata/,eby.adinata
https://www.instagram.com/uncle.yama/,uncle.yama
https://www.instagram.com/medidecil/,medidecil
https://www.instagram.com/micellehalim/,micellehalim
https://www.instagram.com/life.ofgie/,life.ofgie
https://www.instagram.com/yaya_loves_youuu/,yaya_loves_youuu
https://www.instagram.com/anastasia_audreysc/,anastasia_audreysc
https://www.instagram.com/squillliams/,squillliams
https://www.instagram.com/indraparuga/,indraparuga
https://www.instagram.com/emmamadan/,emmamadan
https://www.instagram.com/creafein/,creafein
https://www.instagram.com/jorenzojonathan/,jorenzojonathan
https://www.instagram.com/viggyvino/,viggyvino
https://www.instagram.com/polina.a/,polina.a
https://www.instagram.com/javaphile96/,javaphile96
https://www.instagram.com/thaliaandini/,thaliaandini
https://www.instagram.com/pipigawww/,pipigawww
https://www.instagram.com/missgrandindonesiaofficial/,missgrandindonesiaofficial
https://www.instagram.com/rellkeyy/,rellkeyy
https://www.instagram.com/stampcase.bali/,stampcase.bali
https://www.instagram.com/ayy_andriana/,ayy_andriana
https://www.instagram.com/eizamaghfira/,eizamaghfira
https://www.instagram.com/umaisoumaima/,umaisoumaima
https://www.instagram.com/vtapritia/,vtapritia
https://www.instagram.com/mtriamustika/,mtriamustika
https://www.instagram.com/_sammaxx_/,_sammaxx_
https://www.instagram.com/ariefayip_/,ariefayip_
https://www.instagram.com/nurafarhanaaa/,nurafarhanaaa
https://www.instagram.com/_lukichova_/,_lukichova_
https://www.instagram.com/fathirbahanan/,fathirbahanan
https://www.instagram.com/harishfadhil/,harishfadhil
https://www.instagram.com/fatimahshirin._/,fatimahshirin._
https://www.instagram.com/_forrise/,_forrise
https://www.instagram.com/_haziqj/,_haziqj
https://www.instagram.com/bams_pattikawa/,bams_pattikawa
https://www.instagram.com/wonderbluefreedive/,wonderbluefreedive
https://www.instagram.com/fadithya01/,fadithya01
https://www.instagram.com/diphabarus/,diphabarus
https://www.instagram.com/dimasbestari/,dimasbestari
https://www.instagram.com/reksanalendra/,reksanalendra
https://www.instagram.com/iara.music_/,iara.music_
https://www.instagram.com/iamsararena/,iamsararena
https://www.instagram.com/kumalaambar/,kumalaambar
https://www.instagram.com/frkhayla/,frkhayla
https://www.instagram.com/louisreyner6/,louisreyner6
https://www.instagram.com/_nugeeee/,_nugeeee
https://www.instagram.com/tim_aditya/,tim_aditya
https://www.instagram.com/dv_chivu/,dv_chivu
https://www.instagram.com/edurinaldy/,edurinaldy
https://www.instagram.com/keanu.js/,keanu.js
https://www.instagram.com/lilchindoboi/,lilchindoboi
https://www.instagram.com/dj.fanya/,dj.fanya
https://www.instagram.com/wirsarrr/,wirsarrr
https://www.instagram.com/ghinageriz/,ghinageriz
https://www.instagram.com/rezzarizr/,rezzarizr
https://www.instagram.com/rukes/,rukes
https://www.instagram.com/andryesetiawan/,andryesetiawan
https://www.instagram.com/zicoazi/,zicoazi
https://www.instagram.com/ivana.dusarduyn/,ivana.dusarduyn
https://www.instagram.com/mitchslorach/,mitchslorach
https://www.instagram.com/jelitajee/,jelitajee
https://www.instagram.com/dudutdj/,dudutdj
https://www.instagram.com/nntysxmusic/,nntysxmusic
https://www.instagram.com/nissaoktora/,nissaoktora
https://www.instagram.com/joodakota/,joodakota
https://www.instagram.com/stephenwira/,stephenwira
https://www.instagram.com/kikodwk/,kikodwk
https://www.instagram.com/vifalksatria/,vifalksatria
https://www.instagram.com/cannyclaudya/,cannyclaudya
https://www.instagram.com/kimm.id/,kimm.id
https://www.instagram.com/juliakristie/,juliakristie
https://www.instagram.com/errikirre/,errikirre
https://www.instagram.com/matsumotong/,matsumotong
https://www.instagram.com/joelbanget/,joelbanget
https://www.instagram.com/mhdalfrzl/,mhdalfrzl
https://www.instagram.com/aydra/,aydra
https://www.instagram.com/haryotejo/,haryotejo
https://www.instagram.com/robstee_/,robstee_
https://www.instagram.com/michellejesicaa/,michellejesicaa
https://www.instagram.com/hi.gab/,hi.gab
https://www.instagram.com/damabdz/,damabdz
https://www.instagram.com/sarasabila/,sarasabila
https://www.instagram.com/raramispawanti/,raramispawanti
https://www.instagram.com/sundaysundaemusic/,sundaysundaemusic
https://www.instagram.com/sayhitojesse/,sayhitojesse
https://www.instagram.com/m0r3nd/,m0r3nd
https://www.instagram.com/ivonnemadlenec/,ivonnemadlenec
https://www.instagram.com/dhenadf/,dhenadf
https://www.instagram.com/jirosamin/,jirosamin
https://www.instagram.com/irfiorent/,irfiorent
https://www.instagram.com/nadia.vecchi/,nadia.vecchi
https://www.instagram.com/adstrwn/,adstrwn
https://www.instagram.com/findmevilla/,findmevilla
https://www.instagram.com/yakobuz1/,yakobuz1
https://www.instagram.com/windy_lazuardi/,windy_lazuardi
https://www.instagram.com/tanamur.jpeg/,tanamur.jpeg
https://www.instagram.com/brianrmadhann/,brianrmadhann
https://www.instagram.com/djumcollect/,djumcollect
https://www.instagram.com/deyn.al/,deyn.al
https://www.instagram.com/suedeshots/,suedeshots
https://www.instagram.com/er_erlangga/,er_erlangga
https://www.instagram.com/dhioadhinugra/,dhioadhinugra
https://www.instagram.com/dancesignal/,dancesignal
https://www.instagram.com/riomotret/,riomotret
https://www.instagram.com/abilrie/,abilrie
https://www.instagram.com/jeep_wranglers/,jeep_wranglers
https://www.instagram.com/timothyronaldd/,timothyronaldd
https://www.instagram.com/suliantoindriaputra/,suliantoindriaputra
https://www.instagram.com/rizkyudo/,rizkyudo
https://www.instagram.com/kiesha.alvaro/,kiesha.alvaro
https://www.instagram.com/milesfilms/,milesfilms
https://www.instagram.com/sundarpichai/,sundarpichai
https://www.instagram.com/mariokassarofficial/,mariokassarofficial
https://www.instagram.com/herbert.situmorang.7/,herbert.situmorang.7
https://www.instagram.com/nyfanewyork/,nyfanewyork
https://www.instagram.com/newyorkfilmacademy/,newyorkfilmacademy
https://www.instagram.com/jeep/,jeep
https://www.instagram.com/societyawards/,societyawards
https://www.instagram.com/jeffbezos/,jeffbezos
https://www.instagram.com/babecabiita/,babecabiita
https://www.instagram.com/thisisbillgates/,thisisbillgates
https://www.instagram.com/honda/,honda
https://www.instagram.com/neildegrassetyson/,neildegrassetyson
https://www.instagram.com/grantgust/,grantgust
https://www.instagram.com/jejesoekarno/,jejesoekarno
https://www.instagram.com/nike/,nike
https://www.instagram.com/holidayswap/,holidayswap
https://www.instagram.com/venesia_ari/,venesia_ari
https://www.instagram.com/hightyid/,hightyid
https://www.instagram.com/_adamrajwa/,_adamrajwa
https://www.instagram.com/gwynethgnv/,gwynethgnv
https://www.instagram.com/dodit_mul/,dodit_mul
https://www.instagram.com/its_lauramoane2/,its_lauramoane2
https://www.instagram.com/the_rosemaryy/,the_rosemaryy
https://www.instagram.com/sdambarwati/,sdambarwati
https://www.instagram.com/officialpilarez/,officialpilarez
https://www.instagram.com/arnoldpo/,arnoldpo
https://www.instagram.com/alexpreview/,alexpreview
https://www.instagram.com/samuelchrist/,samuelchrist
https://www.instagram.com/nataliezenn24/,nataliezenn24
https://www.instagram.com/budyceka_bucek/,budyceka_bucek
https://www.instagram.com/afifsalmanalfarisi/,afifsalmanalfarisi
https://www.instagram.com/nthniazefanya/,nthniazefanya
https://www.instagram.com/cahyaidputra/,cahyaidputra
https://www.instagram.com/cristianodslv_/,cristianodslv_
https://www.instagram.com/hendrajunior2022/,hendrajunior2022
https://www.instagram.com/swr_carwash/,swr_carwash
https://www.instagram.com/debrugge_/,debrugge_
https://www.instagram.com/hafiz_husni/,hafiz_husni
https://www.instagram.com/matthew.parulian/,matthew.parulian
https://www.instagram.com/karinasalim/,karinasalim
https://www.instagram.com/asheladz/,asheladz
https://www.instagram.com/graciemgdln/,graciemgdln
https://www.instagram.com/teppanku/,teppanku
https://www.instagram.com/celloszxz/,celloszxz
https://www.instagram.com/astridasuryatenggara/,astridasuryatenggara
https://www.instagram.com/putrimarino/,putrimarino
https://www.instagram.com/zh4vira/,zh4vira
https://www.instagram.com/lyasxh_/,lyasxh_
https://www.instagram.com/aknesalua0904/,aknesalua0904
https://www.instagram.com/wingsgroupsurabaya/,wingsgroupsurabaya
https://www.instagram.com/abunsungkar/,abunsungkar
https://www.instagram.com/muhammadzahirubaydillah/,muhammadzahirubaydillah
https://www.instagram.com/virakoban8302/,virakoban8302
https://www.instagram.com/mculangtahun_arif/,mculangtahun_arif
https://www.instagram.com/da7_robi/,da7_robi
https://www.instagram.com/yoona__lim/,yoona__lim
https://www.instagram.com/mellyleeofficial/,mellyleeofficial
https://www.instagram.com/zaskiadyamecca/,zaskiadyamecca
https://www.instagram.com/azizahsalsha_/,azizahsalsha_
https://www.instagram.com/gadiiing/,gadiiing
https://www.instagram.com/leshclinic/,leshclinic
https://www.instagram.com/levianbillar/,levianbillar
https://www.instagram.com/streamentertainment_/,streamentertainment_
https://www.instagram.com/da5_ebyrizta14/,da5_ebyrizta14
https://www.instagram.com/kyo1122/,kyo1122
https://www.instagram.com/flowirtz/,flowirtz
https://www.instagram.com/leslaragency/,leslaragency
https://www.instagram.com/ryanjiro_/,ryanjiro_
https://www.instagram.com/conorbradley.03/,conorbradley.03
https://www.instagram.com/cuerpoid/,cuerpoid
https://www.instagram.com/fyifact/,fyifact
https://www.instagram.com/dedimulyadi71/,dedimulyadi71
https://www.instagram.com/jck_desaratu/,jck_desaratu
https://www.instagram.com/lida_selfi07/,lida_selfi07
https://www.instagram.com/miloskerkezofficial/,miloskerkezofficial
https://www.instagram.com/mybalqiss/,mybalqiss
https://www.instagram.com/citraciki/,citraciki
https://www.instagram.com/curtisjones/,curtisjones
https://www.instagram.com/kareenakapoorkhan/,kareenakapoorkhan
https://www.instagram.com/da7_sastra08/,da7_sastra08
https://www.instagram.com/flaviozavieraa/,flaviozavieraa
https://www.instagram.com/sridev1206/,sridev1206
https://www.instagram.com/ataliapr/,ataliapr
https://www.instagram.com/leslar_entertainment/,leslar_entertainment
https://www.instagram.com/juliaprt7/,juliaprt7
https://www.instagram.com/prabowo/,prabowo
https://www.instagram.com/duniapunyacerita/,duniapunyacerita
https://www.instagram.com/dinanfajrina/,dinanfajrina
https://www.instagram.com/hidahpratama/,hidahpratama
https://www.instagram.com/leshiativana/,leshiativana
https://www.instagram.com/official_lestilovers_indonesia/,official_lestilovers_indonesia
https://www.instagram.com/muhammadnuzuldzikri/,muhammadnuzuldzikri
https://www.instagram.com/kampunghalamanofficial/,kampunghalamanofficial
https://www.instagram.com/harsiwiachmad/,harsiwiachmad
https://www.instagram.com/ibrahimakonate/,ibrahimakonate
https://www.instagram.com/esterlita_alexander/,esterlita_alexander
https://www.instagram.com/indosiar/,indosiar
https://www.instagram.com/davidsuwarto/,davidsuwarto
https://www.instagram.com/iwanfals/,iwanfals
https://www.instagram.com/amiawards/,amiawards
https://www.instagram.com/bulebarbie_official/,bulebarbie_official
https://www.instagram.com/___aryan___/,___aryan___
https://www.instagram.com/ask.malika/,ask.malika
https://www.instagram.com/hananiagroup.id/,hananiagroup.id
https://www.instagram.com/szoboszlaidominik/,szoboszlaidominik
https://www.instagram.com/kitabisacom/,kitabisacom
https://www.instagram.com/calamaryshop/,calamaryshop
https://www.instagram.com/nitavior/,nitavior
https://www.instagram.com/kajol/,kajol
https://www.instagram.com/adebae.77/,adebae.77
https://www.instagram.com/diana_sastra/,diana_sastra
https://www.instagram.com/melodylaksani92/,melodylaksani92
https://www.instagram.com/leslarrecords/,leslarrecords
https://www.instagram.com/yasminnapper/,yasminnapper
https://www.instagram.com/alex_isak/,alex_isak
https://www.instagram.com/tomcruise/,tomcruise
https://www.instagram.com/pablogavi/,pablogavi
https://www.instagram.com/ustadzabdulsomad_official/,ustadzabdulsomad_official
https://www.instagram.com/dr.iqhbal/,dr.iqhbal
https://www.instagram.com/itsnaufalsamudra/,itsnaufalsamudra
https://www.instagram.com/fakhru_ans_official/,fakhru_ans_official
https://www.instagram.com/endowataru/,endowataru
https://www.instagram.com/callistarum/,callistarum
https://www.instagram.com/marshaz/,marshaz
https://www.instagram.com/plesbol.inc/,plesbol.inc
https://www.instagram.com/aqeelacalista/,aqeelacalista
https://www.instagram.com/shabrina_leonita/,shabrina_leonita
https://www.instagram.com/itsaulia17/,itsaulia17
https://www.instagram.com/arianinismaputri/,arianinismaputri
https://www.instagram.com/alnassr/,alnassr
https://www.instagram.com/nasariastri/,nasariastri
https://www.instagram.com/gyaps/,gyaps
https://www.instagram.com/dinda.ghaniaa/,dinda.ghaniaa
https://www.instagram.com/waodeofficial/,waodeofficial
https://www.instagram.com/ajaib_investasi/,ajaib_investasi
https://www.instagram.com/bellabonita_r.a/,bellabonita_r.a
https://www.instagram.com/syahamimishahri/,syahamimishahri
https://www.instagram.com/noparpradipta_/,noparpradipta_
https://www.instagram.com/vidiodotcom/,vidiodotcom
https://www.instagram.com/bouttier_maxime/,bouttier_maxime
https://www.instagram.com/sanayairani/,sanayairani
https://www.instagram.com/iamdevano/,iamdevano
https://www.instagram.com/dokterfeliani/,dokterfeliani
https://www.instagram.com/da4_fildan/,da4_fildan
https://www.instagram.com/valtifanka/,valtifanka
https://www.instagram.com/itadyahpurnamasari/,itadyahpurnamasari
https://www.instagram.com/thebathaholic/,thebathaholic
https://www.instagram.com/ratuisyellnrzr/,ratuisyellnrzr
https://www.instagram.com/cut.intannabila/,cut.intannabila
https://www.instagram.com/radhikkamadan/,radhikkamadan
https://www.instagram.com/primarasaresto/,primarasaresto
https://www.instagram.com/virgilvandijk/,virgilvandijk
https://www.instagram.com/aaliyah.massaid/,aaliyah.massaid
https://www.instagram.com/24evercoffee/,24evercoffee
https://www.instagram.com/handy.bonny/,handy.bonny
https://www.instagram.com/lyodraofficial/,lyodraofficial
https://www.instagram.com/mulanjameela1/,mulanjameela1
https://www.instagram.com/hrithikroshan/,hrithikroshan
https://www.instagram.com/jajanan.djalu/,jajanan.djalu
https://www.instagram.com/trinityoptima/,trinityoptima
https://www.instagram.com/septiasiregar17/,septiasiregar17
https://www.instagram.com/byayudyahandari/,byayudyahandari
https://www.instagram.com/beingsalmankhan/,beingsalmankhan
https://www.instagram.com/sheiladaisha/,sheiladaisha
https://www.instagram.com/dewiperssik9/,dewiperssik9
https://www.instagram.com/putrasiregarr17/,putrasiregarr17
https://www.instagram.com/lida_ridwan17/,lida_ridwan17
https://www.instagram.com/sherlyannavita/,sherlyannavita
https://www.instagram.com/nandaarsynt/,nandaarsynt
https://www.instagram.com/elsaajapasal/,elsaajapasal
https://www.instagram.com/bellyiverzon/,bellyiverzon
https://www.instagram.com/fadiljaidi/,fadiljaidi
https://www.instagram.com/gia_manek/,gia_manek
https://www.instagram.com/ibuhajat123/,ibuhajat123
https://www.instagram.com/ustadz.pantun/,ustadz.pantun
https://www.instagram.com/anna.mci10/,anna.mci10
https://www.instagram.com/fg_icha/,fg_icha
https://www.instagram.com/ranveersingh/,ranveersingh
https://www.instagram.com/zara_leola_official/,zara_leola_official
https://www.instagram.com/smindrawati/,smindrawati
https://www.instagram.com/amitabhbachchan/,amitabhbachchan
https://www.instagram.com/adele/,adele
https://www.instagram.com/ponijanliaw/,ponijanliaw
https://www.instagram.com/gadiscsadiqah/,gadiscsadiqah
https://www.instagram.com/nehakakkar/,nehakakkar
https://www.instagram.com/ucie_sucita/,ucie_sucita
https://www.instagram.com/dwina_drm/,dwina_drm
https://www.instagram.com/ildivo/,ildivo
https://www.instagram.com/claudiaudie/,claudiaudie
https://www.instagram.com/jokowi/,jokowi
https://www.instagram.com/atykimmorahnew/,atykimmorahnew
https://www.instagram.com/gibran_rakabuming/,gibran_rakabuming
https://www.instagram.com/iranndha/,iranndha
https://www.instagram.com/dinihanipahm/,dinihanipahm
https://www.instagram.com/jennheryanto/,jennheryanto
https://www.instagram.com/hanggini/,hanggini
https://www.instagram.com/alemacallister/,alemacallister
https://www.instagram.com/akshaykumar/,akshaykumar
https://www.instagram.com/celinedion/,celinedion
https://www.instagram.com/harshaalimalhotra_03/,harshaalimalhotra_03
https://www.instagram.com/lyia_tm/,lyia_tm
https://www.instagram.com/3dent_id/,3dent_id
https://www.instagram.com/kayla.nadira/,kayla.nadira
https://www.instagram.com/ginaaayoubi/,ginaaayoubi
https://www.instagram.com/lilyjcollins/,lilyjcollins
https://www.instagram.com/klinikdermaprojakarta/,klinikdermaprojakarta
https://www.instagram.com/7sainaljassmi/,7sainaljassmi
https://www.instagram.com/yellowfitkitchen/,yellowfitkitchen
https://www.instagram.com/kaktyann/,kaktyann
https://www.instagram.com/marlenehariman/,marlenehariman
https://www.instagram.com/mdtv/,mdtv
https://www.instagram.com/sigitwardana/,sigitwardana
https://www.instagram.com/deepikapadukone/,deepikapadukone
https://www.instagram.com/fannysabilaofficial/,fannysabilaofficial
https://www.instagram.com/mimi.peri/,mimi.peri
https://www.instagram.com/elv.label/,elv.label
https://www.instagram.com/daidermawann/,daidermawann
https://www.instagram.com/nonaculinary/,nonaculinary
https://www.instagram.com/sithamarino/,sithamarino
https://www.instagram.com/handemiyy/,handemiyy
https://www.instagram.com/drgdevya/,drgdevya
https://www.instagram.com/fachrulhadid/,fachrulhadid
https://www.instagram.com/nattaama_/,nattaama_
https://www.instagram.com/aruanmarsha/,aruanmarsha
https://www.instagram.com/mawrellous/,mawrellous
https://www.instagram.com/shabrinaaluna/,shabrinaaluna
https://www.instagram.com/elelrumi/,elelrumi
https://www.instagram.com/michan_91/,michan_91
https://www.instagram.com/ikhsanpirdaus1/,ikhsanpirdaus1
https://www.instagram.com/daarulquranindonesia/,daarulquranindonesia
https://www.instagram.com/mahirahkhan/,mahirahkhan
https://www.instagram.com/oliviasumargo/,oliviasumargo
https://www.instagram.com/kana.sybilla/,kana.sybilla
https://www.instagram.com/officialpilarez/,officialpilarez
https://www.instagram.com/aishakeem15/,aishakeem15
https://www.instagram.com/realpz/,realpz
https://www.instagram.com/alifalubis/,alifalubis
https://www.instagram.com/moell.id/,moell.id
https://www.instagram.com/hke57/,hke57
https://www.instagram.com/shafaharris/,shafaharris
https://www.instagram.com/cutputrims/,cutputrims
https://www.instagram.com/priyankachopra/,priyankachopra
https://www.instagram.com/anisarahmaan/,anisarahmaan
https://www.instagram.com/lida_rara06/,lida_rara06
https://www.instagram.com/dwihandaanda/,dwihandaanda
https://www.instagram.com/shraddhakapoor/,shraddhakapoor
https://www.instagram.com/randpunk/,randpunk
https://www.instagram.com/buttonscarves/,buttonscarves
https://www.instagram.com/thariqhalilintar/,thariqhalilintar
https://www.instagram.com/lida_alifaulia02/,lida_alifaulia02
https://www.instagram.com/aliaabhatt/,aliaabhatt
https://www.instagram.com/vidialdiano/,vidialdiano
https://www.instagram.com/rizkinanazarr/,rizkinanazarr
https://www.instagram.com/alexanderbarackel/,alexanderbarackel
https://www.instagram.com/adysky99/,adysky99
https://www.instagram.com/shaniaindryn/,shaniaindryn
https://www.instagram.com/zivamagnolya/,zivamagnolya
https://www.instagram.com/dianamputri/,dianamputri
https://www.instagram.com/vienstasman/,vienstasman
https://www.instagram.com/susansameeh/,susansameeh
https://www.instagram.com/kiranadevina/,kiranadevina
https://www.instagram.com/ferrysal1m/,ferrysal1m
https://www.instagram.com/novitamochamad/,novitamochamad
https://www.instagram.com/tasyafarasya/,tasyafarasya
https://www.instagram.com/sinisukanthony/,sinisukanthony
https://www.instagram.com/gebysrikandii/,gebysrikandii
https://www.instagram.com/bintangemon/,bintangemon
https://www.instagram.com/eriesuzan/,eriesuzan
https://www.instagram.com/okidatanglagi/,okidatanglagi
https://www.instagram.com/bellinamer/,bellinamer
https://www.instagram.com/shaktiarora/,shaktiarora
https://www.instagram.com/shreyaghoshal/,shreyaghoshal
https://www.instagram.com/fahrulrochman_/,fahrulrochman_
https://www.instagram.com/varundvn/,varundvn
https://www.instagram.com/ferry_fernandez83/,ferry_fernandez83
https://www.instagram.com/benkasyafani/,benkasyafani
https://www.instagram.com/amingisback/,amingisback
https://www.instagram.com/rizalakbarazhari/,rizalakbarazhari
https://www.instagram.com/adelia_finsani/,adelia_finsani
https://www.instagram.com/mayshajhu/,mayshajhu
https://www.instagram.com/ayungberinda/,ayungberinda
https://www.instagram.com/shellasaukiaofficial/,shellasaukiaofficial
https://www.instagram.com/femilasinukaban/,femilasinukaban
https://www.instagram.com/arafahrianti/,arafahrianti
https://www.instagram.com/angkringan.tehita/,angkringan.tehita
https://www.instagram.com/hijabchic/,hijabchic
https://www.instagram.com/nisaf__/,nisaf__
https://www.instagram.com/mamah_kejora/,mamah_kejora
https://www.instagram.com/tasya_ratu_gopo/,tasya_ratu_gopo
https://www.instagram.com/bamed.id/,bamed.id
https://www.instagram.com/andyrobertson94/,andyrobertson94
https://www.instagram.com/manutd/,manutd
https://www.instagram.com/ayra.zahra.nursyifa/,ayra.zahra.nursyifa
https://www.instagram.com/kierking8/,kierking8
https://www.instagram.com/findriliasanvira/,findriliasanvira
https://www.instagram.com/chocochipsboutique/,chocochipsboutique
https://www.instagram.com/adindanegara/,adindanegara
https://www.instagram.com/fabioasher/,fabioasher
https://www.instagram.com/afnaalliya_/,afnaalliya_
https://www.instagram.com/sintyamarisca/,sintyamarisca
https://www.instagram.com/sevinc_sevil/,sevinc_sevil
https://www.instagram.com/fraulila/,fraulila
https://www.instagram.com/philipekarunia/,philipekarunia
https://www.instagram.com/siviazizah/,siviazizah
https://www.instagram.com/arie_kriting/,arie_kriting
https://www.instagram.com/anushkasharma/,anushkasharma
https://www.instagram.com/anwar_bab/,anwar_bab
https://www.instagram.com/sherine/,sherine
https://www.instagram.com/putriisnari3/,putriisnari3
https://www.instagram.com/betariayu22/,betariayu22
https://www.instagram.com/dindazani/,dindazani
https://www.instagram.com/mulanisanjay/,mulanisanjay
https://www.instagram.com/alyaaputri/,alyaaputri
https://www.instagram.com/shandyaulia/,shandyaulia
https://www.instagram.com/umar_syarief/,umar_syarief
https://www.instagram.com/ayudyahandari/,ayudyahandari
https://www.instagram.com/drellendr/,drellendr
https://www.instagram.com/natasharizkynew/,natasharizkynew
https://www.instagram.com/luqmanoktaviana_mc/,luqmanoktaviana_mc
https://www.instagram.com/zayn/,zayn
https://www.instagram.com/lida2020_aco1/,lida2020_aco1
https://www.instagram.com/baraa_masoud/,baraa_masoud
https://www.instagram.com/mawaddatulhaq/,mawaddatulhaq
https://www.instagram.com/halobandung/,halobandung
https://www.instagram.com/marshanatika/,marshanatika
https://www.instagram.com/h.hermansuherman/,h.hermansuherman
https://www.instagram.com/eva_ellococg10/,eva_ellococg10
https://www.instagram.com/andirianto_official/,andirianto_official
https://www.instagram.com/mahaliniraharja/,mahaliniraharja
https://www.instagram.com/mariana__putri/,mariana__putri
https://www.instagram.com/abdillah.sholeh/,abdillah.sholeh
https://www.instagram.com/jharnabhagwani/,jharnabhagwani
https://www.instagram.com/dr.najmahnurislami/,dr.najmahnurislami
https://www.instagram.com/laurabbasjackson/,laurabbasjackson
https://www.instagram.com/rey_mbayang/,rey_mbayang
https://www.instagram.com/kesharatuliu05/,kesharatuliu05
https://www.instagram.com/js.collection_official/,js.collection_official
https://www.instagram.com/enazirashf_/,enazirashf_
https://www.instagram.com/patriciagouw/,patriciagouw
https://www.instagram.com/kdi2020_wina/,kdi2020_wina
https://www.instagram.com/riafinola/,riafinola
https://www.instagram.com/revinavt/,revinavt
https://www.instagram.com/tokoleslar/,tokoleslar
https://www.instagram.com/fajarnugrs/,fajarnugrs
https://www.instagram.com/jennifercoppenreal20/,jennifercoppenreal20
https://www.instagram.com/nadiaraysa/,nadiaraysa
https://www.instagram.com/lilymhe/,lilymhe
https://www.instagram.com/lestikejora/,lestikejora
https://www.instagram.com/adiba.knza/,adiba.knza
https://www.instagram.com/sridev1206/,sridev1206
https://www.instagram.com/ndf.s/,ndf.s
https://www.instagram.com/tapia/,tapia
https://www.instagram.com/nasyamarcella/,nasyamarcella
https://www.instagram.com/kitabisacom/,kitabisacom
https://www.instagram.com/emmaraducanu/,emmaraducanu
https://www.instagram.com/dewaopentournament/,dewaopentournament
https://www.instagram.com/nishabasrewan/,nishabasrewan
https://www.instagram.com/kingryan/,kingryan
https://www.instagram.com/jasminmeijers/,jasminmeijers
https://www.instagram.com/bailafauri/,bailafauri
https://www.instagram.com/desta80s/,desta80s
https://www.instagram.com/regina.tanyaa/,regina.tanyaa
https://www.instagram.com/andre_rosiade/,andre_rosiade
https://www.instagram.com/whisnusantika/,whisnusantika
https://www.instagram.com/gyaps/,gyaps
https://www.instagram.com/justjared/,justjared
https://www.instagram.com/jessicashainaa/,jessicashainaa
https://www.instagram.com/eri.carl/,eri.carl
https://www.instagram.com/valtifanka/,valtifanka
https://www.instagram.com/carlitosalcarazz/,carlitosalcarazz
https://www.instagram.com/welber07official/,welber07official
https://www.instagram.com/charles_leclerc/,charles_leclerc
https://www.instagram.com/mariatheodoree/,mariatheodoree
https://www.instagram.com/chelsea.veronnia/,chelsea.veronnia
https://www.instagram.com/aaliyah.massaid/,aaliyah.massaid
https://www.instagram.com/fuji_an/,fuji_an
https://www.instagram.com/zahmuz12/,zahmuz12
https://www.instagram.com/zaraadhsty/,zaraadhsty
https://www.instagram.com/iniadzwaaurell/,iniadzwaaurell
https://www.instagram.com/sultansapta/,sultansapta
https://www.instagram.com/alyssadaguise/,alyssadaguise
https://www.instagram.com/zarworldpadel.id/,zarworldpadel.id
https://www.instagram.com/wimbledon/,wimbledon
https://www.instagram.com/xolovelyayana/,xolovelyayana
https://www.instagram.com/davinaakaramoy/,davinaakaramoy
https://www.instagram.com/adrianarmanasco/,adrianarmanasco
https://www.instagram.com/firdaaindiraa/,firdaaindiraa
https://www.instagram.com/putrasiregarr17/,putrasiregarr17
https://www.instagram.com/gabriellaekaputri/,gabriellaekaputri
https://www.instagram.com/kezialetheia/,kezialetheia
https://www.instagram.com/raissanggiani/,raissanggiani
https://www.instagram.com/fadiljaidi/,fadiljaidi
https://www.instagram.com/leonardmalikiii/,leonardmalikiii
https://www.instagram.com/maudyeffrosina/,maudyeffrosina
https://www.instagram.com/mikha_hernan/,mikha_hernan
https://www.instagram.com/danniasalsabilla/,danniasalsabilla
https://www.instagram.com/karinasalim/,karinasalim
https://www.instagram.com/denise.hoefer.3005/,denise.hoefer.3005
https://www.instagram.com/asnawi_bhr/,asnawi_bhr
https://www.instagram.com/ybrap/,ybrap
https://www.instagram.com/dwina_drm/,dwina_drm
https://www.instagram.com/c.eendy/,c.eendy
https://www.instagram.com/annyaerica/,annyaerica
https://www.instagram.com/nicoleparham_/,nicoleparham_
https://www.instagram.com/paparich666/,paparich666
https://www.instagram.com/alecyavebyy/,alecyavebyy
https://www.instagram.com/alegalan96/,alegalan96
https://www.instagram.com/thomascgibson/,thomascgibson
https://www.instagram.com/gladysvctry/,gladysvctry
https://www.instagram.com/grigordimitrov/,grigordimitrov
https://www.instagram.com/gilangsamiadji/,gilangsamiadji
https://www.instagram.com/rd.ayuregita/,rd.ayuregita
https://www.instagram.com/niloverjudge/,niloverjudge
https://www.instagram.com/fatehhalilintar/,fatehhalilintar
https://www.instagram.com/taufikwahyuda/,taufikwahyuda
https://www.instagram.com/rklopperr/,rklopperr
https://www.instagram.com/ddaffariqq/,ddaffariqq
https://www.instagram.com/angiemstwn/,angiemstwn
https://www.instagram.com/adeleeta/,adeleeta
https://www.instagram.com/marlenehariman/,marlenehariman
https://www.instagram.com/lulalahfah/,lulalahfah
https://www.instagram.com/afniyulindah/,afniyulindah
https://www.instagram.com/malaikha/,malaikha
https://www.instagram.com/racheltheresia/,racheltheresia
https://www.instagram.com/witansulaiman_/,witansulaiman_
https://www.instagram.com/bellaclrs/,bellaclrs
https://www.instagram.com/adipati/,adipati
https://www.instagram.com/mufli_ananda/,mufli_ananda
https://www.instagram.com/just.yumi/,just.yumi
https://www.instagram.com/shela_lala96/,shela_lala96
https://www.instagram.com/harashta/,harashta
https://www.instagram.com/theresaefrata/,theresaefrata
https://www.instagram.com/thariqhalilintar/,thariqhalilintar
https://www.instagram.com/adysky99/,adysky99
https://www.instagram.com/zivamagnolya/,zivamagnolya
https://www.instagram.com/doshzn/,doshzn
https://www.instagram.com/munggaran6/,munggaran6
https://www.instagram.com/aurelialourdes/,aurelialourdes
https://www.instagram.com/rifqiftr/,rifqiftr
https://www.instagram.com/darrelmichelin/,darrelmichelin
https://www.instagram.com/key24bingss/,key24bingss
https://www.instagram.com/milajmlaa/,milajmlaa
https://www.instagram.com/vlrieval/,vlrieval
https://www.instagram.com/desrapercaya/,desrapercaya
https://www.instagram.com/iluminen/,iluminen
https://www.instagram.com/raisyah/,raisyah
https://www.instagram.com/iamdevano/,iamdevano
https://www.instagram.com/egymaulanavikri/,egymaulanavikri
https://www.instagram.com/indiarosebrownn/,indiarosebrownn
https://www.instagram.com/nuffal/,nuffal
https://www.instagram.com/kharimaocha/,kharimaocha
https://www.instagram.com/evarinjanii/,evarinjanii
https://www.instagram.com/aditiyadaffaa_/,aditiyadaffaa_
https://www.instagram.com/ojmo_/,ojmo_
https://www.instagram.com/aqsaaswar/,aqsaaswar
https://www.instagram.com/ney_neo/,ney_neo
https://www.instagram.com/pratamaarhan8/,pratamaarhan8
https://www.instagram.com/mauragbrll/,mauragbrll
https://www.instagram.com/anissaaziza/,anissaaziza
https://www.instagram.com/jonisaputra09/,jonisaputra09
https://www.instagram.com/ekaceluller/,ekaceluller
https://www.instagram.com/zahirahandifaa/,zahirahandifaa
https://www.instagram.com/ragahdo/,ragahdo
https://www.instagram.com/nicholasandrsn/,nicholasandrsn
https://www.instagram.com/joleneemarie/,joleneemarie
https://www.instagram.com/aruanmarsha/,aruanmarsha
https://www.instagram.com/celloszxz/,celloszxz
https://www.instagram.com/bebytsabina/,bebytsabina
https://www.instagram.com/aeroaswar/,aeroaswar
https://www.instagram.com/ataliabunga/,ataliabunga
https://www.instagram.com/zayn/,zayn
https://www.instagram.com/neymarjr/,neymarjr
https://www.instagram.com/shazhaniaa/,shazhaniaa
https://www.instagram.com/medinadinaaa/,medinadinaaa
https://www.instagram.com/vanessaegas/,vanessaegas
https://www.instagram.com/babelrizki/,babelrizki
https://www.instagram.com/ansellmaputri/,ansellmaputri
https://www.instagram.com/dennisgustiputra/,dennisgustiputra
https://www.instagram.com/drgdevya/,drgdevya
https://www.instagram.com/scarlettofficial/,scarlettofficial
https://www.instagram.com/elnandautomo/,elnandautomo
https://www.instagram.com/raissarmdhn/,raissarmdhn
https://www.instagram.com/rizkybillar/,rizkybillar
https://www.instagram.com/ilimaaa_/,ilimaaa_
https://www.instagram.com/andiannsyah/,andiannsyah
https://www.instagram.com/sabreenadressler/,sabreenadressler
https://www.instagram.com/okintph/,okintph
https://www.instagram.com/rifkiantariksa_/,rifkiantariksa_
https://www.instagram.com/naura.ayu/,naura.ayu
https://www.instagram.com/mailmayo_syahputra89/,mailmayo_syahputra89
https://www.instagram.com/maydinahnfh/,maydinahnfh
https://www.instagram.com/ialzimarker/,ialzimarker
https://www.instagram.com/yorikooangln_/,yorikooangln_
https://www.instagram.com/doctorsiska/,doctorsiska
https://www.instagram.com/maswahibb/,maswahibb
https://www.instagram.com/jelitatf/,jelitatf
https://www.instagram.com/timotiusmul/,timotiusmul
https://www.instagram.com/antogriezmann/,antogriezmann
https://www.instagram.com/revashion/,revashion
https://www.instagram.com/kikysaputrii/,kikysaputrii
https://www.instagram.com/kayra.miendra/,kayra.miendra
https://www.instagram.com/sooyon_texture/,sooyon_texture
https://www.instagram.com/rorymcilroy/,rorymcilroy
https://www.instagram.com/ayusarasw/,ayusarasw
https://www.instagram.com/ayunghadid/,ayunghadid
https://www.instagram.com/lorenzoabraham/,lorenzoabraham
https://www.instagram.com/ratu.namira/,ratu.namira
https://www.instagram.com/daraarafah/,daraarafah
https://www.instagram.com/ranggazlaksmana/,ranggazlaksmana
https://www.instagram.com/roxannemorgann/,roxannemorgann
https://www.instagram.com/sabilavirajatii/,sabilavirajatii
https://www.instagram.com/adinda.latieff/,adinda.latieff
https://www.instagram.com/cintaindraa/,cintaindraa
https://www.instagram.com/keanucampora/,keanucampora
https://www.instagram.com/imamjunaaa/,imamjunaaa
https://www.instagram.com/vladimirama/,vladimirama
https://www.instagram.com/tashyanaraysha/,tashyanaraysha
https://www.instagram.com/angiieewilliams/,angiieewilliams
https://www.instagram.com/alvianarrrr/,alvianarrrr
https://www.instagram.com/sharazaaa/,sharazaaa
https://www.instagram.com/coco3_ame9/,coco3_ame9
https://www.instagram.com/giorgino_abraham/,giorgino_abraham
https://www.instagram.com/ningayu_/,ningayu_
https://www.instagram.com/sajidahhalilintar/,sajidahhalilintar
https://www.instagram.com/ariee7/,ariee7
https://www.instagram.com/tommyteja/,tommyteja
https://www.instagram.com/nadhifbasalamah/,nadhifbasalamah
https://www.instagram.com/tercipungcipung/,tercipungcipung
https://www.instagram.com/tissabiani/,tissabiani
https://www.instagram.com/sintyamarisca/,sintyamarisca
https://www.instagram.com/jovitakaren/,jovitakaren
https://www.instagram.com/emilmari0/,emilmari0
https://www.instagram.com/dikta/,dikta
https://www.instagram.com/steffizamoraaa/,steffizamoraaa
https://www.instagram.com/syifahadju/,syifahadju
https://www.instagram.com/arieltatum/,arieltatum
https://www.instagram.com/ray.paramarta/,ray.paramarta
https://www.instagram.com/winstongomez/,winstongomez
https://www.instagram.com/sintaboshoven/,sintaboshoven
https://www.instagram.com/miurachnd/,miurachnd
https://www.instagram.com/bellezaa_17/,bellezaa_17
https://www.instagram.com/riomotret/,riomotret
https://www.instagram.com/diva.azzura/,diva.azzura
https://www.instagram.com/agynessidik/,agynessidik
https://www.instagram.com/zize.official/,zize.official
https://www.instagram.com/mahardikayusuf/,mahardikayusuf
https://www.instagram.com/mirelnajwaa/,mirelnajwaa
https://www.instagram.com/sarahkeihl/,sarahkeihl
https://www.instagram.com/elinaaaaajoerg/,elinaaaaajoerg
https://www.instagram.com/uan.kaisar/,uan.kaisar
https://www.instagram.com/divafadhilam/,divafadhilam
https://www.instagram.com/safeandsoundjkt/,safeandsoundjkt
https://www.instagram.com/luccafauri/,luccafauri
https://www.instagram.com/njwftkryn_/,njwftkryn_
https://www.instagram.com/agthpricilla/,agthpricilla
https://www.instagram.com/richardo_r55/,richardo_r55
https://www.instagram.com/reynaldiraia/,reynaldiraia
https://www.instagram.com/fadlyfsl_/,fadlyfsl_
https://www.instagram.com/ibnuwardani/,ibnuwardani
https://www.instagram.com/drfeninugraha.spgk/,drfeninugraha.spgk
https://www.instagram.com/ariefmuhammad/,ariefmuhammad
https://www.instagram.com/azahhra/,azahhra
https://www.instagram.com/nissyaa/,nissyaa
https://www.instagram.com/cacatengker/,cacatengker
https://www.instagram.com/hilgadoui/,hilgadoui
https://www.instagram.com/loritayoung_mua/,loritayoung_mua
https://www.instagram.com/rifato/,rifato
https://www.instagram.com/aikoyunichi/,aikoyunichi
https://www.instagram.com/diandramarsha/,diandramarsha
https://www.instagram.com/nathalieawantara/,nathalieawantara
https://www.instagram.com/saskiamaritza/,saskiamaritza
https://www.instagram.com/viviinovika/,viviinovika
https://www.instagram.com/collinjavap/,collinjavap
https://www.instagram.com/byisabellefarradiva/,byisabellefarradiva
https://www.instagram.com/ardibakrie/,ardibakrie
https://www.instagram.com/shafarp/,shafarp
https://www.instagram.com/raquelklarkin/,raquelklarkin
https://www.instagram.com/auliaputrifnaaa/,auliaputrifnaaa
https://www.instagram.com/septiningtyas/,septiningtyas
https://www.instagram.com/aufa_nanda/,aufa_nanda
https://www.instagram.com/yendryma/,yendryma
https://www.instagram.com/lucintaluna_manjalita/,lucintaluna_manjalita
https://www.instagram.com/imantdj/,imantdj
https://www.instagram.com/rhenopoetiray/,rhenopoetiray
https://www.instagram.com/rakeshd18/,rakeshd18
https://www.instagram.com/rehanmubarak/,rehanmubarak
https://www.instagram.com/sherylsheinafia/,sherylsheinafia
https://www.instagram.com/lidyapraditta/,lidyapraditta
https://www.instagram.com/timothyallesandro/,timothyallesandro
https://www.instagram.com/ochiipramita/,ochiipramita
https://www.instagram.com/satinezaneta/,satinezaneta
https://www.instagram.com/mputrasetia/,mputrasetia
https://www.instagram.com/riaricis1795/,riaricis1795
https://www.instagram.com/billsatya/,billsatya
https://www.instagram.com/zefanyamalingkas/,zefanyamalingkas
https://www.instagram.com/loexyanta/,loexyanta
https://www.instagram.com/maudyayunda/,maudyayunda
https://www.instagram.com/ussiyfauziah/,ussiyfauziah
https://www.instagram.com/bungapuspaa/,bungapuspaa
https://www.instagram.com/carissaperusset/,carissaperusset
https://www.instagram.com/hassanalaydrus/,hassanalaydrus
https://www.instagram.com/tamiialwi/,tamiialwi
https://www.instagram.com/michelleearuan/,michelleearuan
https://www.instagram.com/tofanarisantoso/,tofanarisantoso
https://www.instagram.com/adlinrambe/,adlinrambe
https://www.instagram.com/derysyaputraraeger/,derysyaputraraeger
https://www.instagram.com/dimasronisaputra/,dimasronisaputra
https://www.instagram.com/putrailhaq/,putrailhaq
https://www.instagram.com/dxdaa/,dxdaa
https://www.instagram.com/febbyrastanty/,febbyrastanty
https://www.instagram.com/g.alqorni/,g.alqorni
https://www.instagram.com/eldynysf/,eldynysf
https://www.instagram.com/emyaghnia/,emyaghnia
https://www.instagram.com/dusan.ph/,dusan.ph
https://www.instagram.com/kxthriana/,kxthriana
https://www.instagram.com/naura21/,naura21
https://www.instagram.com/bubahalfian/,bubahalfian
https://www.instagram.com/arinokitanya/,arinokitanya
https://www.instagram.com/zaglishabrict/,zaglishabrict
https://www.instagram.com/danielwenas/,danielwenas
https://www.instagram.com/keisyalevronka/,keisyalevronka
https://www.instagram.com/sonjamiraa/,sonjamiraa
https://www.instagram.com/aditlubis/,aditlubis
https://www.instagram.com/irzannfaiq/,irzannfaiq
https://www.instagram.com/aryavasco/,aryavasco
https://www.instagram.com/havizadevianjani/,havizadevianjani
https://www.instagram.com/syala.na/,syala.na
https://www.instagram.com/risyabrabo/,risyabrabo
https://www.instagram.com/ispeakbrandedofficial_/,ispeakbrandedofficial_
https://www.instagram.com/luxcrime_id/,luxcrime_id
https://www.instagram.com/marshel_widianto/,marshel_widianto
https://www.instagram.com/ibnuriza/,ibnuriza
https://www.instagram.com/babylanabila/,babylanabila
https://www.instagram.com/pjk.moon9/,pjk.moon9
https://www.instagram.com/irfanfandi17/,irfanfandi17
https://www.instagram.com/elijahkasper/,elijahkasper
https://www.instagram.com/shannongbr/,shannongbr
https://www.instagram.com/prillylatuconsina96/,prillylatuconsina96
https://www.instagram.com/nabillaayumi/,nabillaayumi
https://www.instagram.com/champagnepapi/,champagnepapi
https://www.instagram.com/febriannindyop/,febriannindyop
https://www.instagram.com/kotomi.ozawa/,kotomi.ozawa
https://www.instagram.com/tianamannering/,tianamannering
https://www.instagram.com/spacelux.official/,spacelux.official
https://www.instagram.com/shandypurnamasari/,shandypurnamasari
https://www.instagram.com/alghazali7/,alghazali7
https://www.instagram.com/jeje.poleddicted/,jeje.poleddicted
https://www.instagram.com/sukagerakclub/,sukagerakclub
https://www.instagram.com/ranggayusuf/,ranggayusuf
https://www.instagram.com/gitajanu/,gitajanu
https://www.instagram.com/nikitamirzanimawardi_172/,nikitamirzanimawardi_172
https://www.instagram.com/keviinhugo/,keviinhugo
https://www.instagram.com/pgatour/,pgatour
https://www.instagram.com/boedy_jvs/,boedy_jvs
https://www.instagram.com/razanzu/,razanzu
https://www.instagram.com/rifkyseptiaji/,rifkyseptiaji
https://www.instagram.com/teukuryz/,teukuryz
https://www.instagram.com/victoria_makeupatelier/,victoria_makeupatelier
https://www.instagram.com/rudyadiputra/,rudyadiputra
https://www.instagram.com/syahfaaevg/,syahfaaevg
https://www.instagram.com/zevanyaawee/,zevanyaawee
https://www.instagram.com/raffinagita1717/,raffinagita1717
https://www.instagram.com/muntazhalilintar/,muntazhalilintar
https://www.instagram.com/bifafelicio/,bifafelicio
https://www.instagram.com/granzetta/,granzetta
https://www.instagram.com/nsyakieb85/,nsyakieb85
https://www.instagram.com/shalvarizaldii/,shalvarizaldii
https://www.instagram.com/dr.tirta/,dr.tirta
https://www.instagram.com/ammarsyahdi/,ammarsyahdi
https://www.instagram.com/titipdongkak_reborn/,titipdongkak_reborn
https://www.instagram.com/sibisma/,sibisma
https://www.instagram.com/tya_ariestya/,tya_ariestya
https://www.instagram.com/titi_kamall/,titi_kamall
https://www.instagram.com/azhkalfa/,azhkalfa
https://www.instagram.com/ade_govinda/,ade_govinda
https://www.instagram.com/jennifer_ipel/,jennifer_ipel
https://www.instagram.com/diniyaan/,diniyaan
https://www.instagram.com/darakezia/,darakezia
https://www.instagram.com/rarafauri/,rarafauri
https://www.instagram.com/fazatmandhika/,fazatmandhika
https://www.instagram.com/sakinatama/,sakinatama
https://www.instagram.com/safiraprameswari/,safiraprameswari
https://www.instagram.com/natashalinadla/,natashalinadla
https://www.instagram.com/fahiramira/,fahiramira
https://www.instagram.com/ichsanrindengan/,ichsanrindengan
https://www.instagram.com/ta.nara/,ta.nara
https://www.instagram.com/24olik/,24olik
https://www.instagram.com/mariaasharita/,mariaasharita
https://www.instagram.com/nabiilamhrn/,nabiilamhrn
https://www.instagram.com/yukikt/,yukikt
https://www.instagram.com/amy_r_qanita/,amy_r_qanita
https://www.instagram.com/lamiyazra/,lamiyazra
https://www.instagram.com/chikievers/,chikievers
https://www.instagram.com/ahmadabdul/,ahmadabdul
https://www.instagram.com/aditadiyatma/,aditadiyatma
https://www.instagram.com/rifkykrismon/,rifkykrismon
https://www.instagram.com/evelyntandionoo/,evelyntandionoo
https://www.instagram.com/jonathanandriano/,jonathanandriano
https://www.instagram.com/tivalsalsabilah/,tivalsalsabilah
https://www.instagram.com/leoafandi_/,leoafandi_
https://www.instagram.com/_aldyrizky/,_aldyrizky
https://www.instagram.com/neswerpus/,neswerpus
https://www.instagram.com/haykaly/,haykaly
https://www.instagram.com/unadembler/,unadembler
https://www.instagram.com/ranaesya/,ranaesya
https://www.instagram.com/callie_officialshop/,callie_officialshop
https://www.instagram.com/rajalatuconsina/,rajalatuconsina
https://www.instagram.com/ammar_tsaqif/,ammar_tsaqif
https://www.instagram.com/abrahamandrew29/,abrahamandrew29
https://www.instagram.com/8rooky_/,8rooky_
https://www.instagram.com/renaldypjs/,renaldypjs
https://www.instagram.com/rakhenaputri/,rakhenaputri
https://www.instagram.com/chintyagabriella/,chintyagabriella
https://www.instagram.com/plusninadiana/,plusninadiana
https://www.instagram.com/bernils.3/,bernils.3
https://www.instagram.com/dethahir/,dethahir
https://www.instagram.com/alyamaharannyy/,alyamaharannyy
https://www.instagram.com/tohakarta/,tohakarta
https://www.instagram.com/zaskiasungkar15/,zaskiasungkar15
https://www.instagram.com/olivianuzan/,olivianuzan
https://www.instagram.com/keziajudith/,keziajudith
https://www.instagram.com/angiemiraclee/,angiemiraclee
https://www.instagram.com/krisnkros/,krisnkros
https://www.instagram.com/salshaindradjaja/,salshaindradjaja
https://www.instagram.com/michaelkammerlohrr/,michaelkammerlohrr
https://www.instagram.com/anugrahlindu/,anugrahlindu
https://www.instagram.com/sooyaaa__/,sooyaaa__
https://www.instagram.com/vampirehollie/,vampirehollie
https://www.instagram.com/menelusurimasa/,menelusurimasa
https://www.instagram.com/lestikejora/,lestikejora
https://www.instagram.com/lany/,lany
https://www.instagram.com/dillaljaidi/,dillaljaidi
https://www.instagram.com/abunsungkar/,abunsungkar
https://www.instagram.com/salshabillaadr/,salshabillaadr
https://www.instagram.com/shikuthebrand/,shikuthebrand
https://www.instagram.com/jkt48gracia/,jkt48gracia
https://www.instagram.com/jkt48.kathrina/,jkt48.kathrina
https://www.instagram.com/fandinasutionn/,fandinasutionn
https://www.instagram.com/estapramanita/,estapramanita
https://www.instagram.com/bernadyaribka/,bernadyaribka
https://www.instagram.com/cantikcitra/,cantikcitra
https://www.instagram.com/vonnyfelicia/,vonnyfelicia
https://www.instagram.com/bylizzieparra/,bylizzieparra
https://www.instagram.com/cinema.21/,cinema.21
https://www.instagram.com/imeldatherinne/,imeldatherinne
https://www.instagram.com/changyonggggg/,changyonggggg
https://www.instagram.com/kittendust/,kittendust
https://www.instagram.com/callistarum/,callistarum
https://www.instagram.com/williamroberts08/,williamroberts08
https://www.instagram.com/terangwicaksono/,terangwicaksono
https://www.instagram.com/shakiranajwa/,shakiranajwa
https://www.instagram.com/er1ca/,er1ca
https://www.instagram.com/bazaarindonesia/,bazaarindonesia
https://www.instagram.com/fsmgmt.id/,fsmgmt.id
https://www.instagram.com/yasaminjasem/,yasaminjasem
https://www.instagram.com/zaraadhsty/,zaraadhsty
https://www.instagram.com/jourdy.pranata/,jourdy.pranata
https://www.instagram.com/jethro.armand/,jethro.armand
https://www.instagram.com/ntsana/,ntsana
https://www.instagram.com/viranada_wd/,viranada_wd
https://www.instagram.com/aaliyah.massaid/,aaliyah.massaid
https://www.instagram.com/angga/,angga
https://www.instagram.com/xolovelyayana/,xolovelyayana
https://www.instagram.com/davinaakaramoy/,davinaakaramoy
https://www.instagram.com/idgitaf/,idgitaf
https://www.instagram.com/adrianarmanasco/,adrianarmanasco
https://www.instagram.com/nadiyarawil/,nadiyarawil
https://www.instagram.com/rintiksedu/,rintiksedu
https://www.instagram.com/vidiooriginals/,vidiooriginals
https://www.instagram.com/venemapictures/,venemapictures
https://www.instagram.com/mikha_hernan/,mikha_hernan
https://www.instagram.com/bondol.jpg/,bondol.jpg
https://www.instagram.com/bryandomani_bd_/,bryandomani_bd_
https://www.instagram.com/aphrodit.a/,aphrodit.a
https://www.instagram.com/mawar_eva/,mawar_eva
https://www.instagram.com/raisyabawazier/,raisyabawazier
https://www.instagram.com/abellyc/,abellyc
https://www.instagram.com/caitlinhalderman/,caitlinhalderman
https://www.instagram.com/kaay.raw/,kaay.raw
https://www.instagram.com/wshusen/,wshusen
https://www.instagram.com/claudiaudie/,claudiaudie
https://www.instagram.com/loveable.redaksi/,loveable.redaksi
https://www.instagram.com/deryzky/,deryzky
https://www.instagram.com/raihaanun/,raihaanun
https://www.instagram.com/wardahbeauty/,wardahbeauty
https://www.instagram.com/kylakameron/,kylakameron
https://www.instagram.com/raniaayamin/,raniaayamin
https://www.instagram.com/shabrinaaluna/,shabrinaaluna
https://www.instagram.com/nkcthi/,nkcthi
https://www.instagram.com/nadialaydrus/,nadialaydrus
https://www.instagram.com/cha_schagerl/,cha_schagerl
https://www.instagram.com/michimomo/,michimomo
https://www.instagram.com/adipati/,adipati
https://www.instagram.com/jesicaceren/,jesicaceren
https://www.instagram.com/alwifachry/,alwifachry
https://www.instagram.com/luthfiaulia/,luthfiaulia
https://www.instagram.com/cakecaine/,cakecaine
https://www.instagram.com/galihsoedirdjo/,galihsoedirdjo
https://www.instagram.com/nianaguerrero/,nianaguerrero
https://www.instagram.com/liarahmat13/,liarahmat13
https://www.instagram.com/yosiemauliza/,yosiemauliza
https://www.instagram.com/just.yumi/,just.yumi
https://www.instagram.com/amandarawles/,amandarawles
https://www.instagram.com/vidialdiano/,vidialdiano
https://www.instagram.com/lauvsongs/,lauvsongs
https://www.instagram.com/wodecase.id/,wodecase.id
https://www.instagram.com/marshatimothy/,marshatimothy
https://www.instagram.com/greciasuhardi/,greciasuhardi
https://www.instagram.com/jejesoekarno/,jejesoekarno
https://www.instagram.com/zivamagnolya/,zivamagnolya
https://www.instagram.com/nandaarsynt/,nandaarsynt
https://www.instagram.com/vondear/,vondear
https://www.instagram.com/omardaniel_/,omardaniel_
https://www.instagram.com/yogaarizona/,yogaarizona
https://www.instagram.com/danialrifki/,danialrifki
https://www.instagram.com/ditodarmawan__/,ditodarmawan__
https://www.instagram.com/faizvishal/,faizvishal
https://www.instagram.com/dwisasono/,dwisasono
https://www.instagram.com/randymartinnn/,randymartinnn
https://www.instagram.com/clarinnaputri/,clarinnaputri
https://www.instagram.com/twindararasati/,twindararasati
https://www.instagram.com/blackpinkofficial/,blackpinkofficial
https://www.instagram.com/azela.putri/,azela.putri
https://www.instagram.com/hasyakyla/,hasyakyla
https://www.instagram.com/linda_darmawan03/,linda_darmawan03
https://www.instagram.com/ojmo_/,ojmo_
https://www.instagram.com/abberahman85/,abberahman85
https://www.instagram.com/jaiiibruh/,jaiiibruh
https://www.instagram.com/claudiasulewski/,claudiasulewski
https://www.instagram.com/khivaiskak/,khivaiskak
https://www.instagram.com/chikifawzi/,chikifawzi
https://www.instagram.com/gheaindrawari/,gheaindrawari
https://www.instagram.com/anaoctarina/,anaoctarina
https://www.instagram.com/patricialourence/,patricialourence
https://www.instagram.com/philipekarunia/,philipekarunia
https://www.instagram.com/siviazizah/,siviazizah
https://www.instagram.com/time.international/,time.international
https://www.instagram.com/niapriskilla/,niapriskilla
https://www.instagram.com/js_khairen/,js_khairen
https://www.instagram.com/galabbythahira/,galabbythahira
https://www.instagram.com/danniasalsabilla/,danniasalsabilla
https://www.instagram.com/zahwaqilah/,zahwaqilah
https://www.instagram.com/anarghia/,anarghia
https://www.instagram.com/bebytsabina/,bebytsabina
https://www.instagram.com/farhanrasyidd/,farhanrasyidd
https://www.instagram.com/odaniooo/,odaniooo
https://www.instagram.com/ansellmaputri/,ansellmaputri
https://www.instagram.com/riacinnamon/,riacinnamon
https://www.instagram.com/gushcloudid/,gushcloudid
https://www.instagram.com/raissarmdhn/,raissarmdhn
https://www.instagram.com/nisacookie/,nisacookie
https://www.instagram.com/halidbadjri_fs/,halidbadjri_fs
https://www.instagram.com/jakecgoss/,jakecgoss
https://www.instagram.com/kesharatuliu05/,kesharatuliu05
https://www.instagram.com/raniamarchella/,raniamarchella
https://www.instagram.com/aruanmarsha/,aruanmarsha
https://www.instagram.com/mvppictures_id/,mvppictures_id
https://www.instagram.com/bojvoyej/,bojvoyej
https://www.instagram.com/rezachandika/,rezachandika
https://www.instagram.com/davaheinzsyahry/,davaheinzsyahry
https://www.instagram.com/sandypradana88/,sandypradana88
https://www.instagram.com/naura.ayu/,naura.ayu
https://www.instagram.com/natasharyder/,natasharyder
https://www.instagram.com/alodita/,alodita
https://www.instagram.com/refalhady/,refalhady
https://www.instagram.com/arash_buana/,arash_buana
https://www.instagram.com/kiaraleswara/,kiaraleswara
https://www.instagram.com/ratnajuni/,ratnajuni
https://www.instagram.com/ninakpw/,ninakpw
https://www.instagram.com/zidnylthfa/,zidnylthfa
https://www.instagram.com/ericaputrii/,ericaputrii
https://www.instagram.com/yurayunita/,yurayunita
https://www.instagram.com/nadhira.ulya/,nadhira.ulya
https://www.instagram.com/vaurindaaisha/,vaurindaaisha
https://www.instagram.com/tynadwijayanti/,tynadwijayanti
https://www.instagram.com/nadyamaudy/,nadyamaudy
https://www.instagram.com/bellagap/,bellagap
https://www.instagram.com/jusuf_long/,jusuf_long
https://www.instagram.com/sarahayuh_/,sarahayuh_
https://www.instagram.com/jehaku.official/,jehaku.official
https://www.instagram.com/keshyavlr/,keshyavlr
https://www.instagram.com/amandasmess/,amandasmess
https://www.instagram.com/jeremiemoeremans/,jeremiemoeremans
https://www.instagram.com/aratst/,aratst
https://www.instagram.com/annetteedoarda/,annetteedoarda
https://www.instagram.com/feliandreca/,feliandreca
https://www.instagram.com/daraarafah/,daraarafah
https://www.instagram.com/sharstagramm/,sharstagramm
https://www.instagram.com/barliasmara/,barliasmara
https://www.instagram.com/graceayuari/,graceayuari
https://www.instagram.com/roses_are_rosie/,roses_are_rosie
https://www.instagram.com/antonioblancojr/,antonioblancojr
https://www.instagram.com/shireeenz/,shireeenz
https://www.instagram.com/dagelan/,dagelan
https://www.instagram.com/dindakirana.s/,dindakirana.s
https://www.instagram.com/nadyaaqilla/,nadyaaqilla
https://www.instagram.com/adikaraf/,adikaraf
https://www.instagram.com/indrabrasco/,indrabrasco
https://www.instagram.com/fomstudio_/,fomstudio_
https://www.instagram.com/rsn.dw/,rsn.dw
https://www.instagram.com/braynlim/,braynlim
https://www.instagram.com/saniachia/,saniachia
https://www.instagram.com/reginaaphx/,reginaaphx
https://www.instagram.com/jenniferchrstie/,jenniferchrstie
https://www.instagram.com/tissabiani/,tissabiani
https://www.instagram.com/alikaislamadina/,alikaislamadina
https://www.instagram.com/ifanhartanto/,ifanhartanto
https://www.instagram.com/jovitakaren/,jovitakaren
https://www.instagram.com/modynz/,modynz
https://www.instagram.com/dikta/,dikta
https://www.instagram.com/steffizamoraaa/,steffizamoraaa
https://www.instagram.com/syifahadju/,syifahadju
https://www.instagram.com/rurypadwa/,rurypadwa
https://www.instagram.com/kevinardillova/,kevinardillova
https://www.instagram.com/m.olndo/,m.olndo
https://www.instagram.com/deboys13/,deboys13
https://www.instagram.com/tiaratrdp_/,tiaratrdp_
https://www.instagram.com/elinaaaaajoerg/,elinaaaaajoerg
https://www.instagram.com/lulu_anggriani/,lulu_anggriani
https://www.instagram.com/lalalalisa_m/,lalalalisa_m
https://www.instagram.com/noldapocha/,noldapocha
https://www.instagram.com/ghazi_alhabsyi/,ghazi_alhabsyi
https://www.instagram.com/ariirhamm/,ariirhamm
https://www.instagram.com/stefanytalita/,stefanytalita
https://www.instagram.com/riomotret/,riomotret
https://www.instagram.com/naziracnoer/,naziracnoer
https://www.instagram.com/awdella/,awdella
https://www.instagram.com/natasharizkynew/,natasharizkynew
https://www.instagram.com/patragumala/,patragumala
https://www.instagram.com/ersyaurel/,ersyaurel
https://www.instagram.com/komengkemong/,komengkemong
https://www.instagram.com/mpok.atiek/,mpok.atiek
https://www.instagram.com/arcollectionn_/,arcollectionn_
https://www.instagram.com/diyanahnurra/,diyanahnurra
https://www.instagram.com/ranzkyle/,ranzkyle
https://www.instagram.com/megandomani1410/,megandomani1410
https://www.instagram.com/joviadhiguna/,joviadhiguna
https://www.instagram.com/julianasteph/,julianasteph
https://www.instagram.com/vicymelanie/,vicymelanie
https://www.instagram.com/dorippu/,dorippu
https://www.instagram.com/pauljasonklein/,pauljasonklein
https://www.instagram.com/adiskayl/,adiskayl
https://www.instagram.com/dewanggaelsandro/,dewanggaelsandro
https://www.instagram.com/dermalogia/,dermalogia
https://www.instagram.com/bianca_nelwan/,bianca_nelwan
https://www.instagram.com/kyranayda/,kyranayda
https://www.instagram.com/turahparthayana/,turahparthayana
https://www.instagram.com/pevpearce/,pevpearce
https://www.instagram.com/ariefmuhammad/,ariefmuhammad
https://www.instagram.com/jenniferbachdim/,jenniferbachdim
https://www.instagram.com/fauzan_nasrul/,fauzan_nasrul
https://www.instagram.com/sarahazka/,sarahazka
https://www.instagram.com/princessmegonondo/,princessmegonondo
https://www.instagram.com/marishachacha/,marishachacha
https://www.instagram.com/sandythema/,sandythema
https://www.instagram.com/niaswara_/,niaswara_
https://www.instagram.com/akbaralaziz/,akbaralaziz
https://www.instagram.com/ssseruni/,ssseruni
https://www.instagram.com/ardhitopramono/,ardhitopramono
https://www.instagram.com/tiarapangestika/,tiarapangestika
https://www.instagram.com/zendaya/,zendaya
https://www.instagram.com/tutorialhidub/,tutorialhidub
https://www.instagram.com/cindercella/,cindercella
https://www.instagram.com/tommyprabowo/,tommyprabowo
https://www.instagram.com/vinnagracia/,vinnagracia
https://www.instagram.com/tioradit/,tioradit
https://www.instagram.com/putriayeesha/,putriayeesha
https://www.instagram.com/dessydiniyanti/,dessydiniyanti
https://www.instagram.com/nenagiesta/,nenagiesta
https://www.instagram.com/faynabilalxndr/,faynabilalxndr
https://www.instagram.com/barrykusuma/,barrykusuma
https://www.instagram.com/gita_bhebhita/,gita_bhebhita
https://www.instagram.com/alyaanz/,alyaanz
https://www.instagram.com/ochiipramita/,ochiipramita
https://www.instagram.com/rifankalbuadi7/,rifankalbuadi7
https://www.instagram.com/rozanqaidi/,rozanqaidi
https://www.instagram.com/gracelsyy/,gracelsyy
https://www.instagram.com/shandywilliam_/,shandywilliam_
https://www.instagram.com/satinezaneta/,satinezaneta
https://www.instagram.com/dessey/,dessey
https://www.instagram.com/malidadinda_/,malidadinda_
https://www.instagram.com/andirazh/,andirazh
https://www.instagram.com/anjanidinavdw/,anjanidinavdw
https://www.instagram.com/sentot_sahid/,sentot_sahid
https://www.instagram.com/ussiyfauziah/,ussiyfauziah
https://www.instagram.com/carissaperusset/,carissaperusset
https://www.instagram.com/honeyrobertss_/,honeyrobertss_
https://www.instagram.com/ifyalyssa/,ifyalyssa
https://www.instagram.com/aldymldni/,aldymldni
https://www.instagram.com/luluelhasbu/,luluelhasbu
https://www.instagram.com/abdelachrian/,abdelachrian
https://www.instagram.com/hamidahrachmayanti/,hamidahrachmayanti
https://www.instagram.com/sabinaaksaa/,sabinaaksaa
https://www.instagram.com/sunhairstylist/,sunhairstylist
https://www.instagram.com/almaaurelia/,almaaurelia
https://www.instagram.com/aulion/,aulion
https://www.instagram.com/dewiahmaad/,dewiahmaad
https://www.instagram.com/lelepons/,lelepons
https://www.instagram.com/ninaseptiani/,ninaseptiani
https://www.instagram.com/bima24prasetyo/,bima24prasetyo
https://www.instagram.com/salmaastia/,salmaastia
https://www.instagram.com/moroccanmusthaves/,moroccanmusthaves
https://www.instagram.com/vebbypalwinta/,vebbypalwinta
https://www.instagram.com/jojoanito/,jojoanito
https://www.instagram.com/emyaghnia/,emyaghnia
https://www.instagram.com/diantyy.a/,diantyy.a
https://www.instagram.com/rachelpatricia/,rachelpatricia
https://www.instagram.com/keisyalevronka/,keisyalevronka
https://www.instagram.com/intanmita/,intanmita
https://www.instagram.com/fidelhertamakeup/,fidelhertamakeup
https://www.instagram.com/irzannfaiq/,irzannfaiq
https://www.instagram.com/ilham_nk/,ilham_nk
https://www.instagram.com/rakoprijanto/,rakoprijanto
https://www.instagram.com/megaiskanti/,megaiskanti
https://www.instagram.com/cinta_brian/,cinta_brian
https://www.instagram.com/dermatologistjakarta/,dermatologistjakarta
https://www.instagram.com/filltheblankspace/,filltheblankspace
https://www.instagram.com/rekawijayakusuma/,rekawijayakusuma
https://www.instagram.com/henandrya/,henandrya
https://www.instagram.com/agrasuseno/,agrasuseno
https://www.instagram.com/zulfamaharani/,zulfamaharani
https://www.instagram.com/prillylatuconsina96/,prillylatuconsina96
https://www.instagram.com/jeqaf/,jeqaf
https://www.instagram.com/yclionk/,yclionk
https://www.instagram.com/boimlenno/,boimlenno
https://www.instagram.com/naufalazharr/,naufalazharr
https://www.instagram.com/tianamannering/,tianamannering
https://www.instagram.com/yow.ha/,yow.ha
https://www.instagram.com/pejalankembarr/,pejalankembarr
https://www.instagram.com/eduwart_/,eduwart_
https://www.instagram.com/rahmaniaastrini/,rahmaniaastrini
https://www.instagram.com/abrar_aabs/,abrar_aabs
https://www.instagram.com/rachgoddard/,rachgoddard
https://www.instagram.com/rebeccatamara/,rebeccatamara
https://www.instagram.com/aphang_alimsudio/,aphang_alimsudio
https://www.instagram.com/cassandraslee/,cassandraslee
https://www.instagram.com/wanda_haraa/,wanda_haraa
https://www.instagram.com/naonomnom/,naonomnom
https://www.instagram.com/jakartakonser/,jakartakonser
https://www.instagram.com/ersamayori/,ersamayori
https://www.instagram.com/suciaurelias/,suciaurelias
https://www.instagram.com/kafisilly/,kafisilly
https://www.instagram.com/imaji_zoe/,imaji_zoe
https://www.instagram.com/ichachndra/,ichachndra
https://www.instagram.com/radinindranayaka/,radinindranayaka
https://www.instagram.com/le.roseville/,le.roseville
https://www.instagram.com/umayshahab/,umayshahab
https://www.instagram.com/ryanogilvy/,ryanogilvy
https://www.instagram.com/lamilami.official/,lamilami.official
https://www.instagram.com/vontiansuwandi/,vontiansuwandi
https://www.instagram.com/teukuryz/,teukuryz
https://www.instagram.com/devinaureel/,devinaureel
https://www.instagram.com/quinanitadiva/,quinanitadiva
https://www.instagram.com/letsfreedive_indonesia/,letsfreedive_indonesia
https://www.instagram.com/bembygusti/,bembygusti
https://www.instagram.com/ameliayusanaa/,ameliayusanaa
https://www.instagram.com/ichsanakbar/,ichsanakbar
https://www.instagram.com/nielshepherd/,nielshepherd
https://www.instagram.com/iwanlatiff/,iwanlatiff
https://www.instagram.com/wear.shoera/,wear.shoera
https://www.instagram.com/salshardls/,salshardls
https://www.instagram.com/sandysandyprasetyo/,sandysandyprasetyo
https://www.instagram.com/shareefadaanish/,shareefadaanish
https://www.instagram.com/agnesnaomi/,agnesnaomi
https://www.instagram.com/dheaseto/,dheaseto
https://www.instagram.com/adityaharivonda/,adityaharivonda
https://www.instagram.com/nataliezenn24/,nataliezenn24
https://www.instagram.com/joyagh/,joyagh
https://www.instagram.com/raffinagita1717/,raffinagita1717
https://www.instagram.com/nagrapakusadewo/,nagrapakusadewo
https://www.instagram.com/dianferdisa/,dianferdisa
https://www.instagram.com/im.amru/,im.amru
https://www.instagram.com/wanikayrie/,wanikayrie
https://www.instagram.com/sarahtuff_/,sarahtuff_
https://www.instagram.com/desmondamos/,desmondamos
https://www.instagram.com/irsyachendikiawan/,irsyachendikiawan
https://www.instagram.com/juicy.jacobb/	juicy.jacobb
https://www.instagram.com/lordleothelazypom/,	lordleothelazypom
https://www.instagram.com/duniagames.co.id/,	duniagames.co.id
https://www.instagram.com/stockwise.id/,	stockwise.id
https://www.instagram.com/timothyronaldd/,	timothyronaldd
https://www.instagram.com/bc.8a41121a/,	bc.8a41121a
https://www.instagram.com/ternakklip/,	ternakklip
https://www.instagram.com/hoootdogs/,	hoootdogs
https://www.instagram.com/griffmass/,	griffmass
https://www.instagram.com/jidion_/,	jidion_
https://www.instagram.com/theeuropeankid/,	theeuropeankid
https://www.instagram.com/vincedi.gg/,	vincedi.gg
https://www.instagram.com/jaygettinbreadofficial/,	jaygettinbreadofficial
https://www.instagram.com/artistswithoutautotune_/,	artistswithoutautotune_
https://www.instagram.com/laclynnkimmm/,	laclynnkimmm
https://www.instagram.com/steinfeldpups/,	steinfeldpups
https://www.instagram.com/half.inch.hero/,	half.inch.hero
https://www.instagram.com/oliviarodrigo/,	oliviarodrigo
https://www.instagram.com/breakingbottlesasmr/,	breakingbottlesasmr
https://www.instagram.com/impracticaljokersofficial/,	impracticaljokersofficial
https://www.instagram.com/fakeprankstv/,	fakeprankstv
https://www.instagram.com/sadiesink_/,	sadiesink_
https://www.instagram.com/taylorswift/,	taylorswift
https://www.instagram.com/prankdisplay/,	prankdisplay
https://www.instagram.com/vitalythegoat/,	vitalythegoat
https://www.instagram.com/ejaak15/,	ejaak15
https://www.instagram.com/saratheyh/,	saratheyh
https://www.instagram.com/manusianlangit/,	manusianlangit
https://www.instagram.com/its_lauramoane2/,	its_lauramoane2
https://www.instagram.com/howaboutbeirut/,	howaboutbeirut
https://www.instagram.com/intrusiveprankz/,	intrusiveprankz
https://www.instagram.com/akbarry/,	akbarry
https://www.instagram.com/lennymilleryt/,	lennymilleryt
https://www.instagram.com/xmtthwkm/,	xmtthwkm
https://www.instagram.com/tobyyesman/,	tobyyesman
https://www.instagram.com/eva.pepaj/,	eva.pepaj
https://www.instagram.com/mar.leh4/,	mar.leh4
https://www.instagram.com/whoselineisitanywaysscene/,	whoselineisitanywaysscene
https://www.instagram.com/samuelchrist/,	samuelchrist
https://www.instagram.com/yeno.bros/,	yeno.bros
https://www.instagram.com/getpovd/,	getpovd
https://www.instagram.com/viralvideo.club/,	viralvideo.club
https://www.instagram.com/zopletv/,	zopletv
https://www.instagram.com/brotherk.magic/,	brotherk.magic
https://www.instagram.com/gebiann/,	gebiann
https://www.instagram.com/tyler.wrightttt/,	tyler.wrightttt
https://www.instagram.com/travque/,	travque
https://www.instagram.com/jaxemfilmz/,	jaxemfilmz
https://www.instagram.com/ayamgils/,	ayamgils
https://www.instagram.com/officialdomthetroll/,	officialdomthetroll
https://www.instagram.com/__vector__/,	__vector__
https://www.instagram.com/realcarlyjaane/,	realcarlyjaane
https://www.instagram.com/tamaradai/,	tamaradai
https://www.instagram.com/misfitmindss/,	misfitmindss
https://www.instagram.com/stevenschapiro/,	stevenschapiro
https://www.instagram.com/christina.and.the.dane/,	christina.and.the.dane
https://www.instagram.com/hikarieee/,	hikarieee
https://www.instagram.com/hypnomotion/,	hypnomotion
https://www.instagram.com/resthamhrani/,	resthamhrani
https://www.instagram.com/steven__wongso/,	steven__wongso
https://www.instagram.com/agengcarlitos/,	agengcarlitos
https://www.instagram.com/fansdetacu/,	fansdetacu
https://www.instagram.com/nikolaisavic/,	nikolaisavic
https://www.instagram.com/helsadriy/,	helsadriy
https://www.instagram.com/willyy.dzn/,	willyy.dzn
https://www.instagram.com/meisyasallwa/,	meisyasallwa
https://www.instagram.com/rachmadiandaffa/,	rachmadiandaffa
https://www.instagram.com/reynaldoatmajaa/,	reynaldoatmajaa
https://www.instagram.com/fauzizfau/,	fauzizfau
https://www.instagram.com/adjisdoaibu/,	adjisdoaibu
https://www.instagram.com/mattymoellz/,	mattymoellz
https://www.instagram.com/marshallmccraw/,	marshallmccraw
https://www.instagram.com/silchancrayon/,	silchancrayon
https://www.instagram.com/arrofiramadhan/,	arrofiramadhan
https://www.instagram.com/kemaspakez/,	kemaspakez
https://www.instagram.com/jerhemynemo/,	jerhemynemo
https://www.instagram.com/felix.siauw/,	felix.siauw
https://www.instagram.com/agentofchaos01_/,	agentofchaos01_
https://www.instagram.com/itsbindasbanda/,	itsbindasbanda
https://www.instagram.com/mikesw_01/,	mikesw_01
https://www.instagram.com/firufd/,	firufd
https://www.instagram.com/kiidkatze/,	kiidkatze
https://www.instagram.com/qorygore/,	qorygore
https://www.instagram.com/razzaqlocks/,	razzaqlocks
https://www.instagram.com/cheekyboyos/,	cheekyboyos
https://www.instagram.com/formerteenheartthrob/,	formerteenheartthrob
https://www.instagram.com/dyes_n_goodvibes/,	dyes_n_goodvibes
https://www.instagram.com/lase.tiar/	lase.tiar
https://www.instagram.com/dzawin_nur/	dzawin_nur
https://www.instagram.com/khalill.l/	khalill.l
https://www.instagram.com/deham4ik/	deham4ik
https://www.instagram.com/kataliokrishna/	kataliokrishna
https://www.instagram.com/zachcray/	zachcray
https://www.instagram.com/lulalahfah/	lulalahfah
https://www.instagram.com/msqiwiie/	msqiwiie
https://www.instagram.com/supercoolben/	supercoolben
https://www.instagram.com/angiemstwn/	angiemstwn
https://www.instagram.com/wantsandneedsbrand_/	wantsandneedsbrand_
https://www.instagram.com/meshvirwani/	meshvirwani
https://www.instagram.com/gemaaw/	gemaaw
https://www.instagram.com/beranikotor.ind/	beranikotor.ind
https://www.instagram.com/qiwiie/	qiwiie
https://www.instagram.com/yuliabaltschun/	yuliabaltschun
https://www.instagram.com/sptrakori_/	sptrakori_
https://www.instagram.com/sebastianjern/	sebastianjern
https://www.instagram.com/beibygabriella/	beibygabriella
https://www.instagram.com/kelvinrahardja/	kelvinrahardja
https://www.instagram.com/lexa_pranker/	lexa_pranker
https://www.instagram.com/rolansihombing_/	rolansihombing_
https://www.instagram.com/suryaabianto/	suryaabianto
https://www.instagram.com/the.jokels/	the.jokels
https://www.instagram.com/ivanlafofficial/	ivanlafofficial
https://www.instagram.com/wirya_h/	wirya_h
https://www.instagram.com/oiaflol/	oiaflol
https://www.instagram.com/richardtheodoreofficial/	richardtheodoreofficial
https://www.instagram.com/chrogman/	chrogman
https://www.instagram.com/ditalimandza/	ditalimandza
https://www.instagram.com/erioarriom/	erioarriom
https://www.instagram.com/cloutom/	cloutom
https://www.instagram.com/haekaalapr/	haekaalapr
https://www.instagram.com/takassassin_/	takassassin_
https://www.instagram.com/danijackel/	danijackel
https://www.instagram.com/tanjun.house/	tanjun.house
https://www.instagram.com/mariaxzhang/	mariaxzhang
https://www.instagram.com/swee.tie_pie/	swee.tie_pie
https://www.instagram.com/rigensih/	rigensih
https://www.instagram.com/arianteo/	arianteo
https://www.instagram.com/laafaa00/	laafaa00
https://www.instagram.com/shdrtlk/	shdrtlk
https://www.instagram.com/jlaservideo/	jlaservideo
https://www.instagram.com/roy.muhammad_/	roy.muhammad_
https://www.instagram.com/johnmichaelhowell/	johnmichaelhowell
https://www.instagram.com/nurdinone/	nurdinone
https://www.instagram.com/ryannatanaels/	ryannatanaels
https://www.instagram.com/jeremiahmiller/	jeremiahmiller
https://www.instagram.com/rock_abbeydawn/	rock_abbeydawn
https://www.instagram.com/jerryinchina111/	jerryinchina111
https://www.instagram.com/hudafatc/	hudafatc
https://www.instagram.com/geraldxliu/	geraldxliu
https://www.instagram.com/vegasmatt/	vegasmatt
https://www.instagram.com/zharif.dk/	zharif.dk
https://www.instagram.com/norajoy_official/	norajoy_official
https://www.instagram.com/official_hyphonix/	official_hyphonix
https://www.instagram.com/nandaprmana/	nandaprmana
https://www.instagram.com/tyleroliveiraofficial/	tyleroliveiraofficial
https://www.instagram.com/lilouruel/	lilouruel
https://www.instagram.com/renzorage/	renzorage
https://www.instagram.com/alipbaihak/	alipbaihak
https://www.instagram.com/arrul_munyenyo/	arrul_munyenyo
https://www.instagram.com/fadhilodonggg/	fadhilodonggg
https://www.instagram.com/kulinernyaberdua/	kulinernyaberdua
https://www.instagram.com/israelpadilla__/	israelpadilla__
https://www.instagram.com/hungryhungryhanny/	hungryhungryhanny
https://www.instagram.com/sayyidasknh/	sayyidasknh
https://www.instagram.com/falyeah/	falyeah
https://www.instagram.com/3gpmelii/	3gpmelii
https://www.instagram.com/fahrezaos/	fahrezaos
https://www.instagram.com/javierstoy/	javierstoy
https://www.instagram.com/wjswhdtj94/	wjswhdtj94
https://www.instagram.com/iqbalembam/	iqbalembam
https://www.instagram.com/hunt2funny/	hunt2funny
https://www.instagram.com/vincentekaluis/	vincentekaluis
https://www.instagram.com/tristansocial/	tristansocial
https://www.instagram.com/bigmoskyy/	bigmoskyy
https://www.instagram.com/rabbertanimations/	rabbertanimations
https://www.instagram.com/bradyshepherdd/	bradyshepherdd
https://www.instagram.com/bata.efendi/	bata.efendi
https://www.instagram.com/justdanigoat/	justdanigoat
https://www.instagram.com/ginasnoer/	ginasnoer
https://www.instagram.com/imamfathur26_/	imamfathur26_
https://www.instagram.com/tiarapangestika/	tiarapangestika
https://www.instagram.com/algifaryiqbal/	algifaryiqbal
https://www.instagram.com/alfntrst/	alfntrst
https://www.instagram.com/gjlsentertainment/	gjlsentertainment
https://www.instagram.com/gugunbeke/	gugunbeke
https://www.instagram.com/del.venture/	del.venture
https://www.instagram.com/onebitebigbite/	onebitebigbite
https://www.instagram.com/megahardiantiii/	megahardiantiii
https://www.instagram.com/screenplayed/	screenplayed
https://www.instagram.com/andrewkalaweit/	andrewkalaweit
https://www.instagram.com/its_fajarrr/	its_fajarrr
https://www.instagram.com/ramdhanigunawan/	ramdhanigunawan
https://www.instagram.com/cingky8801/	cingky8801
https://www.instagram.com/verrestarea/	verrestarea
https://www.instagram.com/howsongsarecreated/	howsongsarecreated
https://www.instagram.com/kevsilalahi/	kevsilalahi
https://www.instagram.com/karynbukankarny/	karynbukankarny
https://www.instagram.com/ger.aldy/	ger.aldy
https://www.instagram.com/gema.bhn/	gema.bhn
https://www.instagram.com/nauradinaa/	nauradinaa
https://www.instagram.com/nottalejandro/	nottalejandro
https://www.instagram.com/nadianingrat/	nadianingrat
https://www.instagram.com/juansennnnn/	juansennnnn
https://www.instagram.com/puldeng9/	puldeng9
https://www.instagram.com/tylillebergg/	tylillebergg
https://www.instagram.com/wilsonsinai/	wilsonsinai
https://www.instagram.com/sherninanuneno/	sherninanuneno
https://www.instagram.com/cipsyi/	cipsyi
https://www.instagram.com/thief.busters/	thief.busters
https://www.instagram.com/rfadil.c/	rfadil.c
https://www.instagram.com/julioekspor/	julioekspor
https://www.instagram.com/danielbayu_/	danielbayu_
https://www.instagram.com/arachive_/	arachive_
https://www.instagram.com/naura_bahri1/	naura_bahri1
https://www.instagram.com/najafatimah/	najafatimah
https://www.instagram.com/benjiro_world/	benjiro_world
https://www.instagram.com/adepranantasembiring366/	adepranantasembiring366
https://www.instagram.com/igamassardi/	igamassardi
https://www.instagram.com/jakecherryy/	jakecherryy
https://www.instagram.com/yogaakurnia/	yogaakurnia
https://www.instagram.com/comenclose/	comenclose
https://www.instagram.com/jason_jht/	jason_jht
https://www.instagram.com/marbella.gracia/	marbella.gracia
https://www.instagram.com/wolfgangpoker/	wolfgangpoker
https://www.instagram.com/raimlaode/	raimlaode
https://www.instagram.com/chrishenry/	chrishenry
https://www.instagram.com/kevin.teguhjaya/	kevin.teguhjaya
https://www.instagram.com/cucopuffs/	cucopuffs
https://www.instagram.com/avfasq/	avfasq
https://www.instagram.com/alwishihabbb/	alwishihabbb
https://www.instagram.com/1vannn.x/	1vannn.x
https://www.instagram.com/mamangosa/	mamangosa
https://www.instagram.com/rizkyaltss/	rizkyaltss
https://www.instagram.com/gjlsworld/	gjlsworld
https://www.instagram.com/kingrizky77/	kingrizky77
https://www.instagram.com/nadyagotami/	nadyagotami
https://www.instagram.com/devinkosasih_/	devinkosasih_
https://www.instagram.com/gyan.im/	gyan.im
https://www.instagram.com/pranksty/	pranksty
https://www.instagram.com/winettaceliaa/	winettaceliaa
https://www.instagram.com/daggy_94/	daggy_94
https://www.instagram.com/haslan.b.i/	haslan.b.i
https://www.instagram.com/sluggshop/	sluggshop
https://www.instagram.com/heyselcuk/	heyselcuk
https://www.instagram.com/iqy__avril/	iqy__avril
https://www.instagram.com/capunnggg/	capunnggg
https://www.instagram.com/maharanifbrynt_/	maharanifbrynt_
https://www.instagram.com/savanahmosss/	savanahmosss
https://www.instagram.com/itsfanyanya/	itsfanyanya
https://www.instagram.com/cokipardedebebas/	cokipardedebebas
https://www.instagram.com/ariidwan/	ariidwan
https://www.instagram.com/galanggjr_/	galanggjr_
https://www.instagram.com/raflyrfl/	raflyrfl
https://www.instagram.com/iggessng/	iggessng
https://www.instagram.com/bankii_ii/	bankii_ii
https://www.instagram.com/syifaahusen/	syifaahusen
https://www.instagram.com/gushy_ent/	gushy_ent
https://www.instagram.com/semakindidevan/	semakindidevan
https://www.instagram.com/saintdavin/	saintdavin
https://www.instagram.com/nyonyamanis.bdg/	nyonyamanis.bdg
https://www.instagram.com/bratty.gbaby/	bratty.gbaby
https://www.instagram.com/graceevoryyy/	graceevoryyy
https://www.instagram.com/lahwfofficial/	lahwfofficial
https://www.instagram.com/thepaparock/	thepaparock
https://www.instagram.com/beachcrimes.mp3/	beachcrimes.mp3
https://www.instagram.com/ryannn_.17/	ryannn_.17
https://www.instagram.com/sgtaditya/	sgtaditya
https://www.instagram.com/lacy.himself/	lacy.himself
https://www.instagram.com/si.artha/	si.artha
https://www.instagram.com/hilfifahrezi/	hilfifahrezi
https://www.instagram.com/nettygadja/	nettygadja
https://www.instagram.com/qoqsik1/	qoqsik1
https://www.instagram.com/egafaizal_/	egafaizal_
https://www.instagram.com/hansmikrefin/	hansmikrefin
https://www.instagram.com/theyloveatak/	theyloveatak
https://www.instagram.com/gimanamii/	gimanamii
https://www.instagram.com/tb_singgih/	tb_singgih
https://www.instagram.com/bewsanddogs/	bewsanddogs
https://www.instagram.com/zeeshan_eating01/	zeeshan_eating01
https://www.instagram.com/aidanmeoww/	aidanmeoww
https://www.instagram.com/adaproject.ig/	adaproject.ig
https://www.instagram.com/ociooo2345/	ociooo2345
https://www.instagram.com/bayuprasetyo_____/	bayuprasetyo_____
https://www.instagram.com/ilhamsetyadiii/	ilhamsetyadiii
https://www.instagram.com/chandrayc/	chandrayc
https://www.instagram.com/dog_training_austin/	dog_training_austin
https://www.instagram.com/_shervy/	_shervy
https://www.instagram.com/diianabella_/	diianabella_
https://www.instagram.com/thalithaw/	thalithaw
https://www.instagram.com/anindiayungts/	anindiayungts
https://www.instagram.com/berill_hoere/	berill_hoere
https://www.instagram.com/rainiersfamily/	rainiersfamily
https://www.instagram.com/degentwinzz/	degentwinzz
https://www.instagram.com/alputrafz/	alputrafz
https://www.instagram.com/agres.id/	agres.id
https://www.instagram.com/ireneswnd/	ireneswnd
https://www.instagram.com/rhnachmad/	rhnachmad
https://www.instagram.com/aryonosibiw/	aryonosibiw
https://www.instagram.com/catharinachrsti/	catharinachrsti
https://www.instagram.com/rafiarlnsyh/	rafiarlnsyh
https://www.instagram.com/rismaharun/	rismaharun
https://www.instagram.com/tciramisu/	tciramisu
https://www.instagram.com/reskeyrava/	reskeyrava
https://www.instagram.com/amazinggilang/	amazinggilang
https://www.instagram.com/sultanucok_/	sultanucok_
https://www.instagram.com/renaldoar/	renaldoar
https://www.instagram.com/aegyoalan/	aegyoalan
https://www.instagram.com/pulsepost1/	pulsepost1
https://www.instagram.com/mannythemanzz/	mannythemanzz
https://www.instagram.com/ardan_achsya/	ardan_achsya
https://www.instagram.com/kevin_tjen/	kevin_tjen
https://www.instagram.com/blakebachert/	blakebachert
https://www.instagram.com/rezadhrmptr/	rezadhrmptr
https://www.instagram.com/hanscahyawan/	hanscahyawan
https://www.instagram.com/drplantsss/	drplantsss
https://www.instagram.com/aldiadit/	aldiadit
https://www.instagram.com/putraap__/	putraap__
https://www.instagram.com/talithajesenia/	talithajesenia
https://www.instagram.com/aryanovrianus/	aryanovrianus
https://www.instagram.com/clararichie283/	clararichie283
https://www.instagram.com/babycarlyjanee/	babycarlyjanee
https://www.instagram.com/a.ndrean___/	a.ndrean___
https://www.instagram.com/mariachristy/	mariachristy
https://www.instagram.com/wigionggopribadi/	wigionggopribadi
https://www.instagram.com/thurldes/	thurldes
https://www.instagram.com/alltrollings/	alltrollings
https://www.instagram.com/derielalf/	derielalf
https://www.instagram.com/rereanggara/	rereanggara
https://www.instagram.com/alexchaniagoo/	alexchaniagoo
https://www.instagram.com/everydaywe.see/	everydaywe.see
https://www.instagram.com/nandasetyap_/	nandasetyap_
https://www.instagram.com/benazzzouz/	benazzzouz
https://www.instagram.com/bocoran_nomer_togel/	bocoran_nomer_togel
https://www.instagram.com/vincents_l/	vincents_l
https://www.instagram.com/devishinta77/	devishinta77
https://www.instagram.com/auraaaaw/	auraaaaw
https://www.instagram.com/leonicojoedo/	leonicojoedo
https://www.instagram.com/officialozkan/	officialozkan
https://www.instagram.com/dandy__aw/,	dandy__aw
https://www.instagram.com/woodyrman/,	woodyrman
https://www.instagram.com/tsaa.van/,	tsaa.van
https://www.instagram.com/itzwyattt/,	itzwyattt
https://www.instagram.com/nuriljigur/,	nuriljigur
https://www.instagram.com/saharabbb99/,	saharabbb99
https://www.instagram.com/cindokw_/	cindokw_
https://www.instagram.com/zie.brb/	zie.brb
https://www.instagram.com/rivicooktavia/	rivicooktavia
https://www.instagram.com/immanuel_mg/,	immanuel_mg
https://www.instagram.com/balqisachoirie/,	balqisachoirie
https://www.instagram.com/wahyuimdn/,	wahyuimdn
https://www.instagram.com/yohansture/,	yohansture"""

# Fungsi untuk mendapatkan rekomendasi calon klien dengan loading 10 detik
def get_recommendations_with_loading(num_recommendations=12):
    """Mendapatkan rekomendasi calon klien dengan loading 10 detik"""
    # Simulasi loading 10 detik
    time.sleep(10)
    
    instagram_df = pd.read_csv(StringIO(INSTAGRAM_DATA))
    
    if len(instagram_df) == 0:
        return pd.DataFrame(columns=['Username', 'Link Instagram'])
    
    # Ambil sampel acak dari data
    if len(instagram_df) <= num_recommendations:
        return instagram_df.sample(n=len(instagram_df))
    else:
        return instagram_df.sample(n=num_recommendations)

# Header utama
st.markdown('<h1 class="main-header">Parthaistic - Dashboard Rekomendasi Calon Klien</h1>', unsafe_allow_html=True)

# Hero Section
st.markdown("""
<div class="hero-section">
    <h2 class="hero-title">Temukan Calon Klien Terbaik</h2>
    
</div>
""", unsafe_allow_html=True)

# Stats Section
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #1e293b; margin-bottom: 1.5rem;'>Statistik Database</h3>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="stats-card">
        <div class="stats-number">850+</div>
        <div class="stats-label">Profil Instagram</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="stats-card">
        <div class="stats-number">100%</div>
        <div class="stats-label">Terverifikasi</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="stats-card">
        <div class="stats-number">🎯</div>
        <div class="stats-label">Presisi Tinggi</div>
    </div>
    """, unsafe_allow_html=True)

# Pencarian Section
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #1e293b; margin-bottom: 1.5rem;'>Mulai Pencarian Calon Klien</h3>", unsafe_allow_html=True)

# Tombol pencarian utama
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("🔍 Mulai Pencarian Calon Klien", use_container_width=True, type="primary"):
        st.session_state['search_triggered'] = True
        st.session_state['loading_start_time'] = time.time()

# Cek jika pencarian sudah dipicu
if 'search_triggered' in st.session_state and st.session_state['search_triggered']:
    # Tampilkan loading sederhana
    with st.spinner("Mencari calon klien terbaik..."):
        # Progress bar
        progress_bar = st.progress(0)
        for i in range(100):
            time.sleep(0.1)  # Loading 10 detik total
            progress_bar.progress(i + 1)
    
    # Dapatkan rekomendasi
    recommendations = get_recommendations_with_loading(num_recommendations=6)
    
    if len(recommendations) > 0:
        st.markdown(f"""
        <div style="text-align: center;">
            <div class="result-count">Ditemukan {len(recommendations)} calon klien potensial</div>
            <p style="color: #64748b; margin-bottom: 2rem;">
                Berikut adalah rekomendasi calon klien yang cocok dengan profil bisnis Anda:
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Tampilkan rekomendasi dalam grid
        cols = st.columns(3)
        
        for idx, (_, row) in enumerate(recommendations.iterrows()):
            with cols[idx % 3]:
                username = row['Username']
                instagram_link = row['Link Instagram']
                
                st.markdown(f"""
                <div class="recommendation-card">
                    <div class="username-badge">@{username}</div>
                    <div style="margin: 0.8rem 0;">
                        <p style="margin: 0.3rem 0; font-size: 0.95rem; color: #475569;">
                            <strong>Username:</strong> {username}
                        </p>
                    </div>
                    <a href="{instagram_link}" target="_blank" class="instagram-link">
                        📷 Kunjungi Profil Instagram
                    </a>
                </div>
                """, unsafe_allow_html=True)
        
        # Tombol refresh di tengah
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔄 Cari Rekomendasi Lainnya", use_container_width=True):
                st.session_state['search_triggered'] = True
                st.session_state['loading_start_time'] = time.time()
                st.rerun()
        
        # Tips untuk menghubungi calon klien
        st.markdown("""
        <div class="tips-box">
            <div class="tips-title">💡 Tips untuk Menghubungi Calon Klien</div>
            <p style="color: #475569; margin-bottom: 0.5rem;">
                1. <strong>Perkenalkan diri dengan jelas</strong> - Sebutkan nama dan bisnis Anda<br>
                2. <strong>Jelaskan nilai tambah</strong> - Apa yang Anda tawarkan untuk mereka<br>
                3. <strong>Personalisasikan pesan</strong> - Sesuaikan dengan konten mereka<br>
                4. <strong>Follow dan engage</strong> - Ikuti akun mereka dan beri komentar relevan
            </p>
        </div>
        """, unsafe_allow_html=True)