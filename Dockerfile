FROM jupyter/scipy-notebook
LABEL maintainer="Abu Khadeejah Karl <salamcast@gmail.com>"
USER root
COPY MLabsPy /home/${NB_USER}/MLabsPy
COPY examples/*.CSV /home/${NB_USER}/
COPY examples/*.ipynb /home/${NB_USER}/
RUN chown -R ${NB_USER}:users /home/${NB_USER}
RUN rm -rf /home/${NB_USER}/work
# set a password so that you don't need to find the token
RUN echo -e "from notebook.auth import passwd \nprint(\"c.NotebookApp.password = '\" + passwd('MLabsPy') + \"'\")" > /set_passwd.py
RUN python3 /set_passwd.py >> /home/${NB_USER}/.jupyter/jupyter_notebook_config.py
