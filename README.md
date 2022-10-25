# cs4113fa22-project
#### Final project for distributed operating systems. 

# Schedule

<b> first: </b>
* Decide how to create the server side of things.
* (storage data structure, message sending, message receiving) 
* the board might be represented as a matrix, or as an array simulating a matrix
* the gRPC info should be set up correctly to allow RPC from pokemon and trainers alike. 
* the board should keep track of how/when players/pokemon move around. 
<b> second: </b>
* Decide how to create the client (pokemon) side of things.
* how will they decide their moves. 
* how will they accomplish moving from spot to spot 
* how to tell if it's been captured
* how will the pokemon keep track of its moves?
<b> third: </b>
* Decide how to create the client (trainer) side of things. 
* how will they decide their moves? 
* how will they accomplish moving? 
* how to tell if they can capture a pokemon? 
* how will the trainer keep track of its moves? 
<b> fourth: </b>
* create a prototype to test client-server interaction
* test the prototype to see if the pokemon/trainers can move correctly
* test the prototype to see if pokeon/trainers can capture correctly
      
  
  ## Emoji Chooser
  
        * To server will initialize the board by creating a board of size NxN array
        * the array will be populated with pokeon and trainers 
        * the emojis will be kept in a file 
        * the server will choose a unique emoji for each pokemon/trainer by indexing through this file. 
        * The N value will be taken in as a command line arguement argv[1] 
        * The P value will be taken in as a command line arguement argv[2] 
        * The T value will be taken in as a command line arguement argv[3]
        * the N parameter will be used by the server machine to create the board of correct size. 
        * the P parameter will be used by the server to create a set number of pokemon entities
        * the T parameter will be used by the server to create a ser number of trainer entities 
        * the dockercompose will have three servers (board, trianer, pokemon) 
        * the protocol buffer will need to account for
          * checking spaces 
          * moving spaces
          * catching pokemon
          * removing from the board
          * adding to the board
          
          
