class find_facebook(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        # req_class, url, header, search_tag, search_attr, search_key, id_tag, pass_tag, id_, pass_
        self.url = 'http://www.facebook.com/login.php'
        self.header = [('user-agent',
                        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36')]
        self.id_ = "experiment9090@gmail.com"
        self.pass_ = "ypim9090"
        queue = Queue.Queue()


        # self, queue, url, header, search_tag, search_attr, search_key, id_tag, pass_tag, id_, pass_
        YPIMcrawler_login(queue, self.url, self.header, None, None, None, 'email', 'pass', self.id_, self.pass_).start()

        self.broswer = queue.get()

    def run(self):
        global query, conn, lock

        url = "https://www.facebook.com/search/str/" + query + "/keywords_users"
        resp = self.broswer.open(url)  # data = set_cookie_broswer (cookie 값 저장됨)
        html = str(resp.read()).replace("<!--", "").replace("-->", "")
        Soup = BeautifulSoup(html, "html.parser")
        db = model.model(conn)
        # print Soup.prettify()
        data_list = Soup.find_all('div', {"class", "_glj"})
        return_facebook_list = []

        for i in data_list:
            each_data = i.find('div', {"class", "_gll"})
            each_name = each_data.text
            each_url = each_data.a['href']

            each_data = i.find('div', {"class", "_glm"})
            job = each_data.text

            each_data = i.find('div', {"class", "_glo"})
            school = each_data.text

            # title = each_name + ", " +  + ", " + job + ", " + school

            title = each_name + "/ " + job + "/ " + school
            img = "http://www.boatshop24.co.uk/upload/Facebook.png"
            lock.acquire()
            face_data = {"web_site":"facebook","href": each_url, "title": title, "img":img}
            db.tb_detail_insert(query,face_data)
            lock.release()

        print "facebook_end"