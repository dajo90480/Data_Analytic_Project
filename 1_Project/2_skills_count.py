#%%
import ast 
import pandas as pd
import seaborn as sns 
from datasets import load_dataset
import matplotlib.pyplot as plt 
#%%
# Loading Data
dataset = load_dataset('lukebarousse/data_jobs')
df = dataset['train'].to_pandas()


# Data Cleanup
df['job_posted_date'] = pd.to_datetime(df['job_posted_date'])
df['job_skills'] = df['job_skills'].apply(lambda x: ast.literal_eval(x) if pd.notna(x) else x)
# %%
df_US = df[df['job_country'] == 'United States']
# %%
df_skills = df_US.explode('job_skills')

df_skills[['job_title', 'job_skills']]
# %%
df_skills_count = df_skills.groupby(['job_skills', 'job_title_short']).size()

df_skills_count
# %%
type(df_skills_count)
# %%
df_skills_count = df_skills_count.reset_index(name='skill_count')

#%%
df_skills_count.sort_values(by='skill_count', ascending=False, inplace=True)
# %%
df_skills_count
# %%
job_titles = df_skills_count['job_title_short'].unique().tolist()
# %%
job_titles = sorted(job_titles[:3])
# %%
job_titles
# %%
fig, ax = plt.subplots(len(job_titles), 1)

for i, job_title in enumerate(job_titles):
    df_plot = df_skills_count[df_skills_count['job_title_short'] == job_title].head(5)
    df_plot.plot(kind='barh', x='job_skills', y='skill_count', ax=ax[i], title=job_title)
    ax[i].invert_yaxis()
    ax[i].set_ylabel('')
    ax[i].legend().set_visible(False)
    
fig.suptitle('Counts of Top Skills In Job Postings', fontsize=15)
fig.tight_layout(h_pad=0.5) # fix the overlap
plt.show()
# %%
df_job_title_count = df_US['job_title_short'].value_counts().reset_index(name='job_total')
# %%
df_skills_perc = pd.merge(df_skills_count, df_job_title_count, how='left', on='job_title_short')
# %%
df_skills_perc['skill_percent'] = 100 * df_skills_perc['skill_count'] / df_skills_perc['job_total']
# %%
df_skills_perc
# %%
fig, ax = plt.subplots(len(job_titles), 1)

sns.set_theme(style='ticks')

for i, job_title in enumerate(job_titles):
    df_plot = df_skills_perc[df_skills_perc['job_title_short'] == job_title].head(5)
    # df_plot.plot(kind='barh', x='job_skills', y='skill_percent', ax=ax[i], title=job_title)
    #?--USING SNS--
    sns.barplot(data=df_plot, x='skill_percent', y='job_skills', ax=ax[i], hue='skill_count', palette='dark:b_r')
    ax[i].set_title(job_title)
  
    ax[i].set_ylabel('')
    ax[i].set_xlabel('')
    ax[i].get_legend().remove()
    ax[i].set_xlim(0, 78)
    
    for n, v in enumerate(df_plot['skill_percent']):
        ax[i].text(v + 1, n, f'{v:.0f}%', va='center')
        
    if i != len(job_titles) - 1:
        ax[i].set_xticks([])
    
fig.suptitle('Likelihood of Skills Requested in US Job Postings', fontsize=15)
fig.tight_layout(h_pad=0.5) # fix the overlap
plt.show()
# %%
