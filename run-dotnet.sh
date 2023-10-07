#!/bin/bash

sudo systemctl daemon-reload
sudo systemctl start myapp
sudo systemctl enable myapp
