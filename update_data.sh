#!/bin/bash

scp -i /home/parallels/Projet_Thomas_A4_Git.pem /home/parallels/A4/data.csv ec2-user@13.48.3.249:/home/ec2-user/A4/


cd A4
git add .
git commit -m "Mise à jour automatique des données"
git push
