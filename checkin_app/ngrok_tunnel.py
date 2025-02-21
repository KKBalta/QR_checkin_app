from pyngrok import ngrok

# Set your ngrok auth token
ngrok.set_auth_token("2tKVId2nZJ99slW1NCyEw7zPWVd_5wRiz2nm8S63xUKBMkWdj")

# Open a tunnel on port 8000 (or whichever port your Django server uses)
public_url = ngrok.connect(8000)
print("Ngrok tunnel available at:", public_url)

# Optionally, keep the script running so that the tunnel remains open
try:
    input("Press Enter to exit and close the tunnel...\n")
except KeyboardInterrupt:
    pass
finally:
    ngrok.kill()
