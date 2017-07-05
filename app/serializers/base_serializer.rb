class BaseSerializer

    def as_json
        fail ABSTRACT_CLASS_EXCEPTION_MESSAGE
    end

end
