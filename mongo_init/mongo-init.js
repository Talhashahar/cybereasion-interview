// add new user with mongo startup script
db.createUser(
        {
            user: "user1",
            pwd: "cybereason",
            roles: [
                {
                    role: "root",
                    db: "admin"
                }
            ]
        }
);

// parse data.txt file and save the users obj in list, push all users with "InsertMany" cli command
let lines = cat('/data_files/data.txt').split('\n');
let lines_count = lines.length-1; //remove last line from file (empty line)
let users = new Array();
for (let i = 0; i < lines_count; i++)
{
    let line_splited = lines[i].split(', ');
    let user ={};
    //parse line and create dictionary
    for(let j=0,lv=line_splited.length;j<lv;j++)
    {
        let dict_key=line_splited[j].split(': ',2);
        user[dict_key[0]]=dict_key[1];
    }
    users.push(user);
}
//insert all users with 1 mongodb cli
db.users.insertMany(users);