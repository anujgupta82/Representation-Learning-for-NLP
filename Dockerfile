FROM python:2.7-onbuild

CMD jupyter notebook --ip=0.0.0.0 --allow-root
