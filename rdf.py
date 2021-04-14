import time
from tqdm import tqdm 
import itertools as itr
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import traceback
from selenium.webdriver.chrome.options import Options
import pandas as pd 
import re
import glob 
import shutil 
import os

def scrape() :  
    #任意のディレクトリを指定
    download_directory = '/Users/soheikurita/Documents/venv/gene2/'
    download_url = 'https://pubchem.ncbi.nlm.nih.gov/gene/'
    gene_csv = pd.read_csv("Pubchem_gene_text_covid-19.csv")
    for i in range(len(gene_csv["geneid"])):
        current_download_directory = download_directory + str(gene_csv["geneid"][i])
        current_download_url = download_url + str(gene_csv["geneid"][i])
        options = webdriver.ChromeOptions()
        #デフォルトダウンロードフォルダを変更する
        options.add_experimental_option("prefs", {"download.default_directory": current_download_directory})
        #自動テストソフトウェアによって制御されていますというメッセージを非表示にする
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        # 拡張機能の自動更新をさせない（アプリ側の自動アップデートとドライバーの互換性によるエラーを回避）
        options.add_experimental_option('useAutomationExtension', False)
        driver = webdriver.Chrome("/Users/soheikurita/Documents/venv/chromedriver", chrome_options=options)
        try:
            driver.implicitly_wait(10)
            driver.get(current_download_url)
            driver.find_element_by_tag_name('body').click()
            for i in range(1000):
                driver.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)
            time.sleep(10)
            #JAVA SCRIPTの実行
            #ダウンロードボタンを押すために邪魔となっているsticky-barをremoveする
            driver.execute_script("document.getElementsByClassName('sticky-bar')[0].remove();")
            elements = driver.find_elements_by_xpath("//button[@data-action='download-section-menu-open']/span")
            for e in elements:
                e.click()
                save_button = driver.find_elements_by_xpath("//span[text()='Save']")
                save_button[0].click()
                time.sleep(3)
        except:
            traceback.print_exc()
        finally:
            driver.quit()


def mkdir():
    #任意の親ディレクトリに各ファイル用のディレクトリを作成　
    #pdbディレクトリの作成
    l = glob.glob("gene2/**/*_pdb*.csv", recursive = True)
    for i in range(len(l)):
        new_path = shutil.move(l[i], "pdb")
    #tested compounds (bioactivity gene)ディレクトリの作成
    l_bio_gene = glob.glob("gene2/**/*_bioactivity_gene*.csv", recursive = True)
    for i in range(len(l_bio_gene)):
        new_path_bio_gene = shutil.move(l_bio_gene[i], "bioactivity_gene")
    #drugbank drugsディレクトリの作成
    l_drugbank = glob.glob("gene2/**/*_drugbank*.csv", recursive = True)
    for i in range(len(l_drugbank)):
        new_path_drugbank = shutil.move(l_drugbank[i], "drugbank")
    #chembl drugディレクトリの作成
    l_chembl = glob.glob("gene2/**/*_chembldrugtargets*.csv", recursive = True)
    for i in range(len(l_chembl)):
        new_path_chembl = shutil.move(l_chembl[i], "chembldrug")
    #guide to pharmacology ligands ディレクトリ
    l_gtopdb = glob.glob("gene2/**/*_gtopdb*.csv", recursive = True)
    for i in range(len(l_gtopdb)):
        new_path_gtopdb = shutil.move(l_gtopdb[i], "gtopdb")
    #bioassay ディレクトリ
    l_bioassay = glob.glob("gene2/**/*_bioassay*.csv", recursive = True)
    for i in range(len(l_bioassay)):
        new_path_bioassay = shutil.move(l_bioassay[i], "bioassay")
    #ctd gene-disease ディレクトリ
    l_gene_disease = glob.glob("gene2/**/*_ctd_gene_disease*.csv", recursive = True)
    for i in range(len(l_gene_disease)):
        new_path_gene_disease = shutil.move(l_gene_disease[i], "gene_disease")
    #gene-gene interaction ディレクトリ
    l_geneinter = glob.glob("gene2/**/*_geneinteractions*.csv", recursive = True)
    for i in range(len(l_geneinter)):
        new_path_geneinter = shutil.move(l_geneinter[i], "geneinter")
    #drug-gene interaction ディレクトリ
    l_dgidb = glob.glob("gene2/**/*_dgidb*.csv", recursive = True)
    for i in range(len(l_dgidb)):
        new_path_dgidb = shutil.move(l_dgidb[i], "dgidb")
    #ctd chemical-gene interactions ディレクトリ
    l_ctdchemicalgene = glob.glob("gene2/**/*_ctdchemicalgene*.csv", recursive = True)
    for i in range(len(l_ctdchemicalgene)):
        new_path_ctdchemicalgene = shutil.move(l_ctdchemicalgene[i], "ctdchemicalgene")
    #pathwayreaction ディレクトリ
    l_pathwayreaction = glob.glob("gene2/**/*_pathwayreaction*.csv", recursive = True)
    for i in range(len(l_pathwayreaction)):
        new_path_pathwayreaction = shutil.move(l_pathwayreaction[i], "pathwayreaction")
    #pathwayディレクトリ
    l_pathway = glob.glob("gene2/**/*_pathway*.csv", recursive = True)
    for i in range(len(l_pathway)):
        new_path_pathway = shutil.move(l_pathway[i], "pathwaygene")
    #RHEAディレクトリ
    l_rhea = glob.glob("gene2/**/*_rhea*.csv", recursive = True)
    for i in range(len(l_rhea)):
        new_path_rhea = shutil.move(l_rhea[i], "rhea")
    


def make_csv_for_togo():

    #csv内の文字列を分割する必要のあるcolumnsのdict
    columns_dict = {
        'bioactivity_gene': [],
        "bioassay": ["pmids"],
        "chembldrug":["pmids", "dois"],
        "ctdchemicalgene":["pmids"],
        "dgidb":["pmids", "dois"],
        "drugbank":["pmids", "dois"],
        "gene_disease":["pmids", "dois"],
        "gtopdb":["pmids", "dois"],
        "pathwaygene":["pmids"],
        "pathwayreaction":["pmids"],
        "pdb":["pmids", "dois"]
    }
    #RDF作成上必要のないcolumnsのdict
    droplist = [["aidtype", "aidmdate", "hasdrc", "rnai", "acname", "acvalue", "aidsrcname", "cmpdname", "ecs", "repacxn"], \
        ["aiddesc", "aidsrcid", "aidsrcname", "aidmdate", "cids", "sids", "geneids", "aidcategories", "protacxns", "depcatg", "rnai", "ecs", "repacxns", "annotation"], \
            ["srcid", "moa", "action"] , \
                ["genesymbol", "taxname", "interaction"] , \
                    ["srcid", "geneclaimname", "interactionclaimsource", "interactiontypes", "drugclaimname", "drugclaimprimaryname"], \
                        ["srcid", "genesymbol", "drugtype", "druggroup", "drugaction", "targettype", "targetid", "targetcomponent", "targetcomponentname", "generalfunc", "specificfunc"], \
                            ["srcid", "genesymbol", "diseasesrcdb", "directevidence"] , \
                                ["srcid", "ligand", "primarytarget", "type", "action", "units", "affinity", "targetname", "targetspecies", "genesymbol"], \
                                    ["pwtype", "category", "srcid", "extid", "core", "cids", "geneids", "protacxns", "ecs", "annotation"], \
                                        ["cids", "geneids", "protacxns", "ecs"], \
                                            ["resolution", "srcid", "expmethod", "lignme", "cids", "protacxns", "geneids"] ]


    i = 0
    for directory, columns in columns_dict.items():
        #csvファイルは任意のディレクトリに保存
        file_list = glob.glob(f'{directory}/*.csv')
        print(f'Number of files: {len(file_list)}')

        for file_name in file_list:

            df = pd.read_csv(file_name)
            df = df.drop(droplist[i], axis = 1)
            new_df = pd.DataFrame(columns = df.columns)
            fi = os.path.splitext(os.path.basename(file_name))[0]

            for index in tqdm(df.index, desc=file_name):
                data = df.iloc[index].to_dict()
                #一つのセルに|,で区切られた複数のidを分割し、それぞれ新しい行にする
                for data_set in itr.product(*[filter(lambda a: a != '', re.split('[|,]', str(data[column]))) for column in columns]):
                    for column, value in zip(columns, data_set):
                        data[column] = value
                    new_df = new_df.append(data, ignore_index=True)
                    
            new_df.to_csv(f'{directory}_s.csv', index=False, mode='a', header=file_name==file_list[0])
        i += 1

if __name__ == "__main__": 
    scrape()
    mkdir()
    make_csv_for_togo()





