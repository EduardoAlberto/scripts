# tratamentos dos dados 
import pandas as pd
import mysql.connector
import csv
import os 
# diretorio
infile = '/Users/eduardoaandrad/Dropbox/Desenv/Script/csv/datahackers.csv'
outfile = '/Users/eduardoaandrad/Dropbox/Desenv/Script/csv/Alteracao.csv'

cabecalho = [
  'id                                   '
 ,'age                                  '
 ,'gender                               '
 ,'living_in_brasil                     '
 ,'living_state                         '
 ,'born_or_graduated                    '
 ,'degreee_level                        '
 ,'job_situation                        '
 ,'workers_number                       '
 ,'manager                              '
 ,'salary_range                         '
 ,'time_experience_data_science         '
 ,'time_experience_before               '
 ,'is_data_science_professional         '
 ,'linear_regression                    '
 ,'logistic_regression                  '
 ,'glms                                 '
 ,'decision_tree                        '
 ,'random_forest                        '
 ,'neural_networks                      '
 ,'bayesian_inference                   '
 ,'ensemble                             '
 ,'svms                                 '
 ,'cnns                                 '
 ,'rnns                                 '
 ,'hmms                                 '
 ,'gans                                 '
 ,'markov_chains                        '
 ,'nlp                                  '
 ,'gradient_boosted_machines            '
 ,'cluster_analysis                     '
 ,'survival_analysis                    '
 ,'longitudinal_data_analysis           '
 ,'joint_analysis                       '
 ,'no_listed_methods                    '
 ,'sql_01                               '
 ,'r                                    '
 ,'python                               '
 ,'c_sharp                              '
 ,'dotnet                               '
 ,'java                                 '
 ,'julia                                '
 ,'sas_stata                            '
 ,'visual_basic_vba                     '
 ,'scala                                '
 ,'matlab                               '
 ,'php                                  '
 ,'no_listed_languages                  '
 ,'most_used_proggraming_languages      '
 ,'sql_02                               '
 ,'nosql_01                             '
 ,'images                               '
 ,'nlp_01                               '
 ,'videos                               '
 ,'sheets                               '
 ,'other_1                              '
 ,'sql_03                               '
 ,'nosql_02                             '
 ,'imagens_02                           '
 ,'nlp_02                               '
 ,'videos_02                            '
 ,'planilhas                            '
 ,'other_2                              '
 ,'aws                                  '
 ,'gcp                                  '
 ,'azure                                '
 ,'ibm                                  '
 ,'on_premise_servers                   '
 ,'cloud_propria                        '
 ,'other_3                              '
 ,'mysql                                '
 ,'oracle                               '
 ,'sql_server                           '
 ,'aurora                               '
 ,'dynamodb                             '
 ,'coachdb                              '
 ,'cassandra                            '
 ,'mongodb                              '
 ,'mariadb                              '
 ,'datomic                              '
 ,'s3                                   '
 ,'postgresql                           '
 ,'elaticsearch                         '
 ,'db2                                  '
 ,'ms_access                            '
 ,'sqlite                               '
 ,'sybase                               '
 ,'firebase                             '
 ,'vertica                              '
 ,'redis                                '
 ,'neo4j                                '
 ,'google_bigtable                      '
 ,'hbase                                '
 ,'other_4                              '
 ,'microsoft_powerbi                    '
 ,'qlik_view_qlik_sense                 '
 ,'tableau                              '
 ,'metabase                             '
 ,'superset                             '
 ,'redash                               '
 ,'microstrategy                        '
 ,'ibm_analytics_cognos                 '
 ,'sap_business_objects                 '
 ,'oracle_business_intelligence         '
 ,'birst                                '
 ,'looker                               '
 ,'google_data_studio                   '
 ,'only_excel_gsheets                   '
 ,'no_bi_tool_at_work                   '
 ,'other_5                              '
 ,'sql_stored_procedures                '
 ,'apache_airflow                       '
 ,'luigi                                '
 ,'aws_glue                             '
 ,'talend                               '
 ,'pentaho                              '
 ,'alteryx                              '
 ,'oracle_data_integrator               '
 ,'ibm_data_stage                       '
 ,'sap_bw_etl                           '
 ,'siss_sql_server_integration_services '
 ,'other_6                              '
 ,'have_data_warehouse                  '
 ,'google_bigquery                      '
 ,'aws_redshift                         '
 ,'snowflake                            '
 ,'oracle_02                            '
 ,'postgres_mysql                       '
 ,'ibm_02                               '
 ,'teradata                             '
 ,'microsoft_azure                      '
 ,'do_not_know                          '
 ,'other_7                              '
 ,'data_hackers_blog                    '
 ,'data_hackers_podcast                 '
 ,'weekly_newsletter                    '
 ,'slack_channel                        '
 ,'data_hackers_bootcamp                '
 ,'do_not_know_data_hackers             '
 ,'prefered_data_hackers_initiative     '
 ,'telegram_groups                      '
 ,'whatsapp_groups                      '
 ,'youtube_channels                     '
 ,'other_brasilian_blogs                '
 ,'other_slack_channels                 '
 ,'twitter                              '
 ,'abroad_blogs                         '
 ,'abroad_podcasts                      '
 ,'meetups_and_events                   '
 ,'only_data_hackers                    '
 ,'other_8                              '
 ,'udacity                              '
 ,'coursera                             '
 ,'udemy                                '
 ,'height                               '
 ,'edx                                  '
 ,'data_camp                            '
 ,'data_quest                           '
 ,'kaggle_learn                         '
 ,'online_courses                       '
 ,'other_9                              '
 ,'data_science_plataforms_preference   '
 ,'other_10                             '
 ,'draw_participation                   '
 ,'living_macroregion                   '
 ,'origin_macroregion                   '
 ,'anonymized_degree_area               '
 ,'anonymized_market_sector             '
 ,'anonymized_manager_level             '
 ,'anonymized_role                      '               
]  

csv_data = pd.read_csv(infile, sep=';', delimiter=None, names=cabecalho, index_col=None)
print(csv_data)
# gera um novo .csv
csv_data.to_csv(outfile, sep=';')

# # conexao com o banco 
mydb = mysql.connector.connect(user='root',password='mysql',host='0.0.0.0',database='mydesenv')
cur = mydb.cursor()
try:
    with open(outfile, encoding = "ISO-8859-1") as arq:
        csv_data = csv.reader(arq, delimiter=';')
        next(csv_data)
        for row in csv_data:
            cur.execute("""insert into mydesenv.tb_analise_mercado
                                    (
                                             id                                
                                            ,age                               
                                            ,gender                            
                                            ,living_in_brasil                  
                                            ,living_state                      
                                            ,born_or_graduated                 
                                            ,degreee_level                     
                                            ,job_situation                     
                                            ,workers_number                    
                                            ,manager                           
                                            ,salary_range                      
                                            ,time_experience_data_science      
                                            ,time_experience_before            
                                            ,is_data_science_professional      
                                            ,linear_regression                 
                                            ,logistic_regression               
                                            ,glms                              
                                            ,decision_tree                     
                                            ,random_forest                     
                                            ,neural_networks                   
                                            ,bayesian_inference                
                                            ,ensemble                          
                                            ,svms                              
                                            ,cnns                              
                                            ,rnns                              
                                            ,hmms                              
                                            ,gans                              
                                            ,markov_chains                     
                                            ,nlp                               
                                            ,gradient_boosted_machines         
                                            ,cluster_analysis                  
                                            ,survival_analysis                 
                                            ,longitudinal_data_analysis        
                                            ,joint_analysis                    
                                            ,no_listed_methods                 
                                            ,sql_01                            
                                            ,r                                 
                                            ,python                            
                                            ,c_sharp                           
                                            ,dotnet                            
                                            ,java                              
                                            ,julia                             
                                            ,sas_stata                         
                                            ,visual_basic_vba                  
                                            ,scala                             
                                            ,matlab                            
                                            ,php                               
                                            ,no_listed_languages               
                                            ,most_used_proggraming_languages   
                                            ,sql_02                            
                                            ,nosql_01                          
                                            ,images                            
                                            ,nlp_01                            
                                            ,videos                            
                                            ,sheets                            
                                            ,other_1                           
                                            ,sql_03                            
                                            ,nosql_02                          
                                            ,imagens_02                        
                                            ,nlp_02                            
                                            ,videos_02                         
                                            ,planilhas                         
                                            ,other_2                           
                                            ,aws                               
                                            ,gcp                               
                                            ,azure                             
                                            ,ibm                               
                                            ,on_premise_servers                
                                            ,cloud_propria                     
                                            ,other_3                           
                                            ,mysql                             
                                            ,oracle                            
                                            ,sql_server                        
                                            ,aurora                            
                                            ,dynamodb                          
                                            ,coachdb                           
                                            ,cassandra                         
                                            ,mongodb                           
                                            ,mariadb                           
                                            ,datomic                           
                                            ,s3                                
                                            ,postgresql                        
                                            ,elaticsearch                      
                                            ,db2                               
                                            ,ms_access                         
                                            ,sqlite                            
                                            ,sybase                            
                                            ,firebase                          
                                            ,vertica                           
                                            ,redis                             
                                            ,neo4j                             
                                            ,google_bigtable                   
                                            ,hbase                             
                                            ,other_4                           
                                            ,microsoft_powerbi                 
                                            ,qlik_view_qlik_sense              
                                            ,tableau                           
                                            ,metabase                          
                                            ,superset                          
                                            ,redash                            
                                            ,microstrategy                     
                                            ,ibm_analytics_cognos              
                                            ,sap_business_objects              
                                            ,oracle_business_intelligence      
                                            ,birst                             
                                            ,looker                            
                                            ,google_data_studio                
                                            ,only_excel_gsheets                
                                            ,no_bi_tool_at_work                
                                            ,other_5                           
                                            ,sql_stored_procedures             
                                            ,apache_airflow                    
                                            ,luigi                             
                                            ,aws_glue                          
                                            ,talend                            
                                            ,pentaho                           
                                            ,alteryx                           
                                            ,oracle_data_integrator            
                                            ,ibm_data_stage                    
                                            ,sap_bw_etl                        
                                            ,siss_sql_server_integration_services
                                            ,other_6                           
                                            ,have_data_warehouse               
                                            ,google_bigquery                   
                                            ,aws_redshift                      
                                            ,snowflake                         
                                            ,oracle_02                         
                                            ,postgres_mysql                    
                                            ,ibm_02                            
                                            ,teradata                          
                                            ,microsoft_azure                   
                                            ,do_not_know                       
                                            ,other_7                           
                                            ,data_hackers_blog                 
                                            ,data_hackers_podcast              
                                            ,weekly_newsletter                 
                                            ,slack_channel                     
                                            ,data_hackers_bootcamp             
                                            ,do_not_know_data_hackers          
                                            ,prefered_data_hackers_initiative  
                                            ,telegram_groups                   
                                            ,whatsapp_groups                   
                                            ,youtube_channels                  
                                            ,other_brasilian_blogs             
                                            ,other_slack_channels              
                                            ,twitter                           
                                            ,abroad_blogs                      
                                            ,abroad_podcasts                   
                                            ,meetups_and_events                
                                            ,only_data_hackers                 
                                            ,other_8                           
                                            ,udacity                           
                                            ,coursera                          
                                            ,udemy                             
                                            ,height                            
                                            ,edx                               
                                            ,data_camp                         
                                            ,data_quest                        
                                            ,kaggle_learn                      
                                            ,online_courses                    
                                            ,other_9                           
                                            ,data_science_plataforms_preference
                                            ,other_10                          
                                            ,draw_participation                
                                            ,living_macroregion                
                                            ,origin_macroregion                
                                            ,anonymized_degree_area            
                                            ,anonymized_market_sector          
                                            ,anonymized_manager_level          
                                            ,anonymized_role                   

                                ) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
                        %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
                        %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
                        %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
                        %s,%s,%s,%s,%s,%s)""", row[:170]
                        )
            mydb.commit()
        if os.path.exists(outfile):
            os.remove((outfile))
        else:
            print('arquivo não existe !')
except IOError:
    print('Arquivo não encontrado')

                        