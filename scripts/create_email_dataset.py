import email
from email.policy import default
import re
from datetime import datetime
import pandas as pd

class MboxReader:
    """A class to read an mbox file."""
    
    def __init__(self, filename):
        """Initialize with the filename."""
        self.handle = open(filename, 'rb')
        assert self.handle.readline().startswith(b'From ')
    
    def __enter__(self):
        """Enter method for context management."""
        return self
    
    def __exit__(self, exc_type, exc_value, exc_traceback):
        """Exit method for context management."""
        self.handle.close()
    
    def __iter__(self):
        """Iterator method."""
        return iter(self.__next__())
    
    def __next__(self):
        """Next method to parse the mbox file."""
        lines = []
        while True:
            line = self.handle.readline()
            if line == b'' or line.startswith(b'From '):
                yield email.message_from_bytes(b''.join(lines), policy=default)
                if line == b'':
                    break
                lines = []
                continue
            lines.append(line)

def preprocess_mbox(filename):
    """Preprocess mbox file to create training dataset."""
    label_pattern = r'Category\s*([^,]+)(?:,|$)'
    sent_emails = {}
    
    with MboxReader(filename) as mbox:
        for i, message in enumerate(mbox):
            if 'X-Gmail-Labels' in message.keys():
                gmail_label = message["X-Gmail-Labels"]
                
                if ('Important' in gmail_label) or ('Starred' in gmail_label):
                    continue
                
                if ('promotions' in gmail_label) or ('updates' in gmail_label):
                    specific_label = re.search(label_pattern, gmail_label).group(1).strip()
                    sender_name = message['From'].split('<')[0].strip()
                    
                    if message['Delivered-To'] == 'azamat.omu@gmail.com':
                        if message['From'] in sent_emails:
                            sent_emails[message['From']].append({
                                'order': len(sent_emails[message['From']]),
                                'sender_name': sender_name,
                                'subject': message['Subject'],
                                'date': message['Date'],
                                'opened': int('Opened' in message["X-Gmail-Labels"]),
                                'label': specific_label
                            })
                        else:
                            sent_emails[message['From']] = [{
                                'order': 0,
                                'sender_name': sender_name,
                                'subject': message['Subject'],
                                'date': message['Date'],
                                'opened': int('Opened' in message["X-Gmail-Labels"]),
                                'label': specific_label
                            }]
            if i % 1000 == 0:
                print(f'Processed {i} emails...')
    
    return sent_emails

def create_dataset(sent_emails):
    """Create dataset from processed emails."""
    data = {
        "sender": [],
        "opened_emails": [],
        "sent_emails": []
    }
    
    for sender in sent_emails.keys():
        data['sender'].append(sender)
        data['opened_emails'].append(sum([record['opened'] for record in sent_emails[sender]]))
        data['sent_emails'].append(len(sent_emails[sender]))
    
    df = pd.DataFrame(data)
    
    # Remove unnecessary parts from sender column
    df['sender'] = df['sender'].str.split('<').str[0].str.strip()
    
    return df

def update_email_order(email_entries):
    """Update email order based on date."""
    email_entries.sort(key=lambda x: datetime.strptime(x['date'], '%a, %d %b %Y %H:%M:%S %z'))
    
    for index, email_entry in enumerate(email_entries):
        email_entry['order'] = index

def prepare_finetune_data(sent_emails, activation, retention):
    """Prepare fine-tune data for language model."""
    finetune_data = []
    for sender_key in sent_emails.keys():
        for email_info in sent_emails[sender_key]:
            entry = ''
            if email_info['sender_name'] in activation:
                entry += 'activation; '
            elif email_info['sender_name'] in retention:
                entry += 'retention; '
            entry += f'{email_info["label"]}; from {email_info["sender_name"]}; {email_info["order"]}th email sent; '
            entry += f'subject: {email_info["subject"]}'
            finetune_data.append(entry)
    return finetune_data

def write_finetune_data(finetune_data, filename):
    """Write fine-tune data to a file."""
    with open(filename, 'w') as file:
        file.write('\n'.join(finetune_data))

def main():
    """Main function."""
    sent_emails = preprocess_mbox('data/allmail.mbox')
    
    activation = create_dataset(sent_emails)[lambda df: df['opened_emails'] == 0]['sender'].unique()
    retention = create_dataset(sent_emails)[lambda df: df['opened_emails'] > 0]['sender'].unique()
    
    for sender, email_entries in sent_emails.items():
        update_email_order(email_entries)
    
    finetune_data = prepare_finetune_data(sent_emails, activation, retention)
    
    write_finetune_data(finetune_data, 'finetune-emails.txt')

if __name__ == "__main__":
    main()

