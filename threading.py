class StockEngine:
    def __init__(self, company_id):
        self.company_id = company_id
        # Assume self.db is your database connection
        self.db = create_engine('sqlite:///stocks.db')

    def fetch_ohlc_data(self):
        Session = sessionmaker(bind=self.db)
        session = Session()
        ohlc_data = session.query(OHLCData).filter_by(company_id=self.company_id).all()
        session.close()
        return ohlc_data

    def calculate_signals(self, ohlc_data):
        # Your existing calculation logic
        signals = generate_signals(ohlc_data)
        return signals

    def save_signals(self, signals):
        Session = sessionmaker(bind=self.db)
        session = Session()
        for signal in signals:
            session.merge(Signal(company_id=signal['company_id'],
                                 timestamp=signal['timestamp'],
                                 signal=signal['signal']))
        session.commit()
        session.close()

    def process(self):
        ohlc_data = self.fetch_ohlc_data()
        signals = self.calculate_signals(ohlc_data)
        self.save_signals(signals)

    def run(self, interval=60):
        while True:
            self.process()
            time.sleep(interval)
import threading
from concurrent.futures import ThreadPoolExecutor
import time

# Your StockEngine class from above

def run_engine_for_company(company_id):
    engine = StockEngine(company_id)
    engine.run()

def main():
    # Fetch all company IDs
    Session = sessionmaker(bind=create_engine('sqlite:///stocks.db'))
    session = Session()
    company_ids = [company.id for company in session.query(Company).all()]
    session.close()

    # Use ThreadPoolExecutor to manage threads
    with ThreadPoolExecutor(max_workers=len(company_ids)) as executor:
        executor.map(run_engine_for_company, company_ids)

if __name__ == "__main__":
    main()