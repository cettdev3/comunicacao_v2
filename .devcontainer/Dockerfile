FROM mcr.microsoft.com/vscode/devcontainers/python:3.9-bullseye

ENV LANG pt_BR.UTF-8
ENV LC_ALL pt_BR.UTF-8
ENV LANGUAGE pt_BR.UTF-8
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONFAULTHANDLER=1
ENV PYTHONUNBUFFERED=1


ARG APP_USER_NAME
ARG APP_UID
ARG APP_GID
ARG APP_NAME

# RUN adduser --uid $APP_UID --shell /bin/zsh --disabled-password --gecos "" $APP_USER_NAME && chown -R $APP_USER_NAME /home/$APP_USER_NAME

RUN apt-get update && apt-get install git -y

ENV TZ=America/Sao_Paulo
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN dpkg-reconfigure tzdata
RUN apt install -y ntpdate
RUN ntpdate pool.ntp.br


RUN pip install pipenv

RUN apt install -y locales libc-bin locales-all
RUN sed -i '/pt_BR.UTF-8/s/^#//g' /etc/locale.gen \
    && locale-gen en_US en_US.UTF-8 pt_BR pt_BR.UTF-8 \
    && dpkg-reconfigure --frontend noninteractive locales \
    && update-locale LANG=pt_BR.UTF-8 LANGUAGE=pt_BR.UTF-8 LC_ALL=pt_BR.UTF-8

ENV PIPENV_VENV_IN_PROJECT=True
ENV PIPENV_SITE_PACKAGES=True
ENV PATH="/home/$APP_USER_NAME/$APP_NAME/.venv/bin:$PATH"

# RUN \
#     NERDS_FONT_VERSION="2.1.0" \
#     && FONT_DIR=/usr/local/share/fonts \
#     && FIRA_CODE_URL=https://github.com/ryanoasis/nerd-fonts/raw/${NERDS_FONT_VERSION}/patched-fonts/FiraCode \
#     && FIRA_CODE_LIGHT_DOWNLOAD_SHA256="5e0e3b18b99fc50361a93d7eb1bfe7ed7618769f4db279be0ef1f00c5b9607d6" \
#     && FIRA_CODE_REGULAR_DOWNLOAD_SHA256="3771e47c48eb273c60337955f9b33d95bd874d60d52a1ba3dbed924f692403b3" \
#     && FIRA_CODE_MEDIUM_DOWNLOAD_SHA256="42dc83c9173550804a8ba2346b13ee1baa72ab09a14826d1418d519d58cd6768" \
#     && FIRA_CODE_BOLD_DOWNLOAD_SHA256="060d4572525972b6959899931b8685b89984f3b94f74c2c8c6c18dba5c98c2fe" \
#     && FIRA_CODE_RETINA_DOWNLOAD_SHA256="e254b08798d59ac7d02000a3fda0eac1facad093685e705ac8dd4bd0f4961b0b" \
#     && mkdir -p $FONT_DIR \
#     && wget -nv -P $FONT_DIR $FIRA_CODE_URL/Light/complete/Fura%20Code%20Light%20Nerd%20Font%20Complete.ttf \
#     && wget -nv -P $FONT_DIR $FIRA_CODE_URL/Regular/complete/Fura%20Code%20Regular%20Nerd%20Font%20Complete.ttf \
#     && wget -nv -P $FONT_DIR $FIRA_CODE_URL/Medium/complete/Fura%20Code%20Medium%20Nerd%20Font%20Complete.ttf \
#     && wget -nv -P $FONT_DIR $FIRA_CODE_URL/Bold/complete/Fura%20Code%20Bold%20Nerd%20Font%20Complete.ttf \
#     && wget -nv -P $FONT_DIR $FIRA_CODE_URL/Retina/complete/Fura%20Code%20Retina%20Nerd%20Font%20Complete.ttf \
#     && echo "$FIRA_CODE_LIGHT_DOWNLOAD_SHA256 $FONT_DIR/Fura Code Light Nerd Font Complete.ttf" | sha256sum -c - \
#     && echo "$FIRA_CODE_REGULAR_DOWNLOAD_SHA256 $FONT_DIR/Fura Code Regular Nerd Font Complete.ttf" | sha256sum -c - \
#     && echo "$FIRA_CODE_MEDIUM_DOWNLOAD_SHA256 $FONT_DIR/Fura Code Medium Nerd Font Complete.ttf" | sha256sum -c - \
#     && echo "$FIRA_CODE_BOLD_DOWNLOAD_SHA256 $FONT_DIR/Fura Code Bold Nerd Font Complete.ttf" | sha256sum -c - \
#     && echo "$FIRA_CODE_RETINA_DOWNLOAD_SHA256 $FONT_DIR/Fura Code Retina Nerd Font Complete.ttf" | sha256sum -c -

RUN mkdir -p /usr/share/zsh-antigen
RUN curl -L git.io/antigen > /usr/share/zsh-antigen/antigen.zsh

USER $APP_USER_NAME

ENV TERM xterm

# Set the default shell to bash rather than sh
ENV SHELL /bin/zsh

# run the installation script  
RUN wget https://github.com/robbyrussell/oh-my-zsh/raw/master/tools/install.sh -O - | zsh || true

# install powerlevel10k
RUN git clone https://github.com/romkatv/powerlevel10k.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/themes/powerlevel10k

RUN git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting
RUN git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions
RUN git clone https://github.com/zsh-users/zsh-completions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-completions

COPY ./.devcontainer/.zshrc ~/
COPY ./.devcontainer/.p10k.zsh ~/
WORKDIR /home/$APP_USER_NAME/$APP_NAME

CMD [ "tail", "-f", "/dev/null" ]