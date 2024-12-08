CREATE TABLE dim_state (
	StateId INT PRIMARY KEY,
    StateCode VARCHAR(5),
    StateName VARCHAR(50),
	create_date DATETIME ,
	update_date DATETIME
);

CREATE TABLE dim_county (
	CountyId INT PRIMARY KEY,
    CountyFips INT ,
    CountyName VARCHAR(100),
    StateId INT,
	create_date DATETIME ,
	update_date DATETIME,
    FOREIGN KEY (StateId) REFERENCES dim_state(StateId),
);

CREATE TABLE dim_party (
	PartyId INT PRIMARY KEY,
    Party VARCHAR(50),
	create_date DATETIME ,
	update_date DATETIME,
);

CREATE TABLE dim_candidate (
	CandidateId INT PRIMARY KEY,
    Candidate VARCHAR(100) ,
    PartyId INT,
	create_date DATETIME ,
	update_date DATETIME,
    FOREIGN KEY (PartyId) REFERENCES dim_party(PartyId),
);

CREATE TABLE fact_election_results (
    FactId INT PRIMARY KEY, 
    CountyId INT,           
    PartyId INT,            
    CandidateId INT,        
    VoteCount FLOAT,        
    CountyTotalVote INT,    
	create_date DATETIME ,
	update_date DATETIME,
    FOREIGN KEY (CountyId) REFERENCES dim_county(CountyId),
    FOREIGN KEY (PartyId) REFERENCES dim_party(PartyId),
    FOREIGN KEY (CandidateId) REFERENCES dim_candidate(CandidateId)
);