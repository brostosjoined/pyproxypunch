# pyproxypunch
UDP Hole Punching client &amp; server proxy
**This program lets you host & connect to friends to play peer-to-peer games without having to open or redirect any port.**

*Technical details: proxypunch creates a user-friendly UDP proxy/tunnel between two peers by hole punching the user's NAT with a custom STUN-like server which additionally "matchmakes" users based on their internal port rather than their NAT-ed port.*  

## How to use
- Choose between **server** (hosting) and **client** (connecting to a host) by typing `s` or `c`, then pressing `Enter`
- Instructions continue below depending on your choice

##### Server / Hosting

- When prompted for a port, choose any port (if you're not sure, choose any randon number between 10000 and 60000), type it and press `Enter`
- In your game, start your server / start hosting on the port you chose
- Ask your peer to connect to the shown host and port, **the peer must connect with proxypunch as explained below, not directly**
- Wait for the peer to connect, then play & profit
- When you're done playing with this peer, stop hosting, and close the proxypunch window (start it again and repeat the process to play with someone else)
- Next time you run proxypunch, you can simply press `Enter` to use the same settings as last time you connected

##### Client / Connecting to a host

- Wait for the person hosting to send you a host and port to connect to
- Enter the host and port when prompted to by typing it and pressing `Enter`
- In your game, connect to the shown host and port given on the terminal(**not the host and port your peer gave you**) 
- Profit & play
- When you're done playing with this peer, disconnect, and close the proxypunch window (start it again and repeat the process to play with someone else)
- Next time you run proxypunch, you can simply press `Enter` to use the same settings as last time you connected

##### Troubleshooting

- If you experience any issue when restarting proxypunch to play with someone else, try to use a different port every time your run proxypunch
- If you have any other issue or feedback, either contact me on Discord at `brostos` or [open an issue on Github](https://github.com/brostosjoined/pyproxypunch/issues/new) 

# CREDITS
- This code was purely converted from go with the help of [codeconvertai](https://codeconvert.ai/app) and fixing minor bugs. Here is the original go package [proxypunch](https://github.com/delthas/proxypunch) by [delthas](https://github.com/delthas).
