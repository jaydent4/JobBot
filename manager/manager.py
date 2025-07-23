import sqlite3
import importlib
from logging_config import setup_logging
from .args import validate_args, parse
import pandas as pd
import time
from const import Valid_Args, Columns
import datetime


class Manager:
    def __init__(self, sources, job_counter, grp_id):
        self.logger = setup_logging("Manager", "INFO", "INFO", "manager.log")
        self.performance_logger = setup_logging("Manager-performance", "INFO", "INFO", "performance.log")

        self.sources = sources
        self.job_counter = job_counter
        self.grp_id = grp_id
        
        self.scrapers = {}
        self.load_scrapers()
        
        try:
            with sqlite3.connect('./job.db') as self.conn:
                self.cur = self.conn.cursor()

                self.cur.execute(
                    """ CREATE TABLE IF NOT EXISTS jobPostings (
                        job_counter INTEGER PRIMARY KEY,
                        GRP_ID INTEGER NOT NULL,
                        application_link TEXT NOT NULL,
                        id INTEGER,
                        company_name TEXT NOT NULL, 
                        role TEXT NOT NULL, 
                        location TEXT NOT NULL, 
                        date_posted DATE NOT NULL,
                        time_posted TIME, 
                        date_scraped DATE NOT NULL,
                        time_scraped TIME NOT NULL, 
                        scrape_source TEXT NOT NULL,
                        level TEXT NOT NULL
                        );"""
                )

                self.conn.commit()

                print("Table exists.")
        except sqlite3.OperationalError as e:
            print("Failed to create table because:", e)
        
        # # TRYING TO LOAD FAKE DATA AND INSERT INTO DB
        data = pd.read_csv("./manager/fake_data.csv")
        data = data.values.tolist()
        self.update_DB(data)

        for row in self.cur.execute("SELECT * FROM jobPostings ORDER BY job_counter"):
            print(row)

        print("------")
        # # checking queries, but how to make sure we dont' ahve 10! query cases?
        # # queryResult = self.cur.execute("""SELECT * FROM jobPostings 
        # #                                WHERE company_name = 'amazon' (side note: this also works: WHERE company_name in ('amazon'))
        # #                                AND role = 'ML'
        # #                                AND date_posted > '2025-06-01'
        # #                                AND time_posted >= '01:04' (side note can also do: time_posted > '01:04:00.000')
        # #                                """)
        # queryControl = self.cur.execute("""SELECT * FROM jobPostings 
        #                                WHERE company_name = 'google'
        #                                LIMIT 1
        #                                """)
        # for row in queryControl:
        #     print(row)

        # print("---")
        # s1 = """SELECT * FROM jobPostings
        #                       WHERE company_name = 'amazon'
        #                       """        
        # s2 = """SELECT * FROM jobPostings
        #                       WHERE date_posted >= '2025-06-01'
        #                     """
        # L = "LIMIT 2"
        # intersection = s1 + "INTERSECT " + s2 + " " + L
        site = "https://www.google.com/search?q=matplotlib%20linestyles"
        q = self.cur.execute(f"SELECT * FROM jobPostings WHERE application_link = ?", (site, ))

        for row in q:
            print(row)

        # job = [("5","meta","swe","canada","https://www.amazon.com/","2025-05-07","09:10","2025-05-11","05:30","fake","intern")]
        # self.update_DB(job)
        # print("------")
        # for row in self.cur.execute("SELECT * FROM jobPostings ORDER BY id"):
        #     print(row)


    """
    Attempt to load all scrapers from configurations
    """
    def load_scrapers(self) -> None:
        
        for name in self.sources:
            module_name = "scrapers." + name
            try:
                self.logger.info(f'Attempting to load module: {module_name}')
                module = importlib.import_module(module_name)
                scraper = getattr(module, name + "Scraper")
                self.scrapers[name] = scraper(self.sources[name])
                self.logger.info(f"loaded scraper: {module_name}")
            except Exception as e:
                self.logger.error(f'Something occurred while attempting to load {module_name}: {e}')
    
    """
    Args:
        name: name of the scraper/site
    
    Returns:
        list[tuple]: each tuple is a separate job posting, each tuple must contain 10 elements in the order of the columns in the database; if the value canont be scraped, put None
    """
    def scrape(self, name) -> list[tuple] | None:
        if name not in self.scrapers:
            self.logger.error(f'Scraper for {name} does not exist')
            return None
        return self.scrapers[name].scrape(self.job_counter, self.grp_id)


    """
    Args:
        None

    Returns:
        list[tuple]: containing job postings from all scrapers
    """
    def run_scrapers(self) -> list[tuple]:
        result: list[tuple] = []
        for name in self.scrapers.keys():
            start_time = time.time()
            scraper_result = self.scrape(name)
            end_time = time.time()
            elapsed_time = end_time - start_time
            if not scraper_result:
                self.logger.error(f"SCRAPER {name} DOES NOT EXIST")
            else:
                self.performance_logger.info(f'Scraper {name} took {elapsed_time:.4f} seconds to run')
                assert(scraper_result != None) # or else red siggly
                result.extend(scraper_result)
        return result


    """
    Calls scrapers then checks if dB updated
    Args:
        None

    Returns:
        (tuple[bool, tuple]): bool is true if dB updated, bool is false if dB did not update, list containing tuple where each tuple is a jobposting
    """
    def update(self) -> tuple[bool, list[tuple] | None]:
        new_postings = self.run_scrapers()
        if len(new_postings) > 0:
            self.update_DB(new_postings)
            return (True, new_postings)
        else:
            return (False, None)
        
        
    def validate_repeat(self, job_posting: tuple) -> bool:
        link = job_posting[Columns.APPLICATION_LINK.value]
        if link == "NONE" or link == None or link == "":
            self.logger.error(f"must have application link for job: {job_posting}")

        query_str = f"SELECT * FROM jobPostings WHERE application_link = \'{link}\'"
        
        results = self.cur.execute(query_str).fetchall()

        grp_ids = set([r[Columns.GRP_ID.value] for r in results])
        for r in results:
            print(link, r)

        if len(results) == 0:
            return True
        elif len(grp_ids) == 1 and job_posting[Columns.GRP_ID.value] in grp_ids:
            return True
        else:
            self.logger.error(f"this job {job_posting}'s application link already exists in the database")
            return False
        

    def validate_date(self, job_posting:tuple) -> bool:
        assert len(job_posting) == Columns.ARGS_SIZE.value, "Incorrect number of values"
        if datetime.date.fromisoformat(job_posting[Columns.DATE_POSTED.value]):
            return True
        else:
            self.logger.error(f"scraped {job_posting} does not have the correct date_posted format of: YYYY-MM-DD")
            return False
        
    
    """
    Inserts scrapped job postings into the main database
    Args:
        jobpostings (list[tuple]):

    Returns:
        None
    """
    def update_DB(self, job_postings: list[tuple]) -> None:
        for job in job_postings:
            if self.validate_repeat(job) and self.validate_date(job):
                try:
                    self.cur.execute("INSERT INTO jobPostings VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", tuple(job))
                    self.logger.info(f"succesfully inserted scrapped job: {job} into the database")
                    self.conn.commit()
                except Exception as e:
                    self.logger.error(f"Something errored while inserting scrapped job {job} into the main database: {e}")


    def obtain_dB_results(self, query_string: str, count: int) -> list[tuple]:
        out: list[tuple] = []
        while len(out) < count:
            # bugged, we are not going forward
            q_result = self.cur.execute(query_string).fetchall()
            print(q_result)
            job_posting = list(q_result[0])
            job_posting[Columns.LOCATION.value] = [job_posting[Columns.LOCATION.value]]
            for r in q_result[1:]:
                if job_posting[Columns.GRP_ID.value] == r[Columns.GRP_ID.value]:
                    job_posting[Columns.LOCATION.value].append(r[Columns.LOCATION.value])
                else:
                    out.append(tuple(job_posting))
                    job_posting = list(r)                    

        return out
        

    """
    Returns data from the database with respect to flags

    Valid flags:
        --time:
            ex: --time 5
        --company
            ex: --company amazon
        --role
            ex: --role swe
        --location
            ex: --location mento_park 
        --level
            ex: --level intern 
        --count
            ex: --count 10 

    Args:
        args (tuple): args inputted by the user
    
    Returns:
        (list[tuple]): a list of jobpostings; each post is a tuple in the list
    """
    def get_data(self, args: tuple) -> list[tuple] | None:
        alphanum_args:list = []
        for i in range(len(args)):
            arg = args[i]
            if arg.startswith('--'):
                alphanum_args.append(arg)
            else:
                alphanum_args.append(''.join(ch for ch in arg if ch.isalnum()))
        
        self.logger.info(alphanum_args)

        if not validate_args(tuple(alphanum_args)):
            return None
        
        self.logger.info(f"validation stage passed")

        parsed_args = parse(tuple(alphanum_args))

        self.logger.info(f"parsing stage passed")

        count = 1 # default return 1 jobposting from database
        if parsed_args[Valid_Args.COUNT.value] is not None:
            count = parsed_args[Valid_Args.COUNT.value][1]
            if len(alphanum_args) == 2 and alphanum_args[0] == "--count":
                query_str = f"SELECT * FROM jobPostings ORDER BY date_scraped DESC"
                return self.obtain_dB_results(query_str, count)

        base_str = "SELECT * FROM jobPostings WHERE "
        counter = 0
        intersect = " INTERSECT "
        final_query_str = ""

        operator = ">="
        for i in range(len(parsed_args) - 1):
            arg_val = parsed_args[i]
            
            if arg_val != None:
                query_str = base_str + f"{arg_val[0]} " + operator + f" \'{arg_val[1]}\'"
                
                if counter % 2 != 0:
                    query_str = intersect + query_str

                counter += 1
                final_query_str += query_str

                self.logger.info(f"final query currently is: \n{final_query_str}")
            operator = "="

        self.logger.info(f"final query is \n{final_query_str}")
        return self.obtain_dB_results(final_query_str +  " " + "COLLATE NOCASE", count)
    

