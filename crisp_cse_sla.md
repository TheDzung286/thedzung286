First, I created some workflows to get data from webhook of Crisp, including Customer Message, Agent Message, Segment_data, Vistor_data, State_data.
![image](https://github.com/user-attachments/assets/c5b29184-21ab-49df-babf-13443ef4a704)
![image](https://github.com/user-attachments/assets/0cebac53-ac2c-481c-bdd8-2641961c5701)

Then, I match the time that agent replied to customer to calculate the response time
![image](https://github.com/user-attachments/assets/700def3a-7b93-4a94-82ce-38d34d6ace44)

To track the first response time, I created a new table - "crisp_sla" in my database. When a customer initiates a chat, a record is added. I then identify records where the first response time is null and update them accordingly.
![image](https://github.com/user-attachments/assets/74c6983f-7d83-4bec-92cb-3370b813925b)

The State data is for calculating Resolution time. This Index is updated to the table "crisp_sla"
![image](https://github.com/user-attachments/assets/9bf3fbfa-196d-41b2-9761-307846c59f35)

